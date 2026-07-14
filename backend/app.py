import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(__file__))

from agents.enrichment_agent import enrich_prompt
from agents.script_agent import generate_script
from agents.storyboard_agent import generate_storyboard
from agents.video_agent import generate_all_clips
from agents.assembly_agent import assemble_video, get_output_url

from config import DEBUG, PORT

app = Flask(__name__)
CORS(app)

DEFAULT_SCENES = 3


@app.route('/output/<filename>')
def serve_video(filename):
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    return send_from_directory(output_dir, filename)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "running",
        "service": "ReelCraft API",
        "cloud": "Alibaba Cloud",
        "models": {
            "text": "qwen-plus",
            "video": "wan2.2-t2v-plus (Wan)"
        }
    })


# FULL pipeline. If a pre-written 'script' is supplied, it is used as-is
# (user edited it in the preview step) instead of regenerating.
@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        topic = data.get('topic', '').strip()
        genre = data.get('genre', 'drama').strip()
        num_scenes = int(data.get('num_scenes', DEFAULT_SCENES))
        provided_script = data.get('script', '').strip()

        if not topic and not provided_script:
            return jsonify({"error": "Topic or script is required"}), 400

        print(f"\n{'='*50}")
        print(f"NEW GENERATION | Topic: {topic} | Scenes: {num_scenes}")
        print(f"{'='*50}\n")

        # STAGE 0: Enrich (still done for the demo transform display + vibe)
        print("STAGE 0: Enriching prompt...")
        enrichment = enrich_prompt(topic) if topic else {"enriched": "", "vibe": "cinematic"}
        enriched_prompt = enrichment["enriched"]
        vibe = enrichment["vibe"]
        print(f"Vibe: {vibe}\n")

        # STAGE 1: Script — use provided edited script if present
        if provided_script:
            print("STAGE 1: Using provided (edited) script")
            script = provided_script
        else:
            print("STAGE 1: Generating script...")
            script = generate_script(enriched_prompt, vibe=vibe, num_scenes=num_scenes)
        print("Script ready\n")

        # STAGE 2: Storyboard
        print("STAGE 2: Generating storyboard...")
        storyboard = generate_storyboard(script, num_scenes=num_scenes)
        scene_prompts = storyboard["scenes"]
        bible = storyboard["bible"]
        print(f"Storyboard: {len(scene_prompts)} shots\n")

        if not scene_prompts:
            return jsonify({"error": "Storyboard produced no scenes"}), 500

        # STAGE 3: Video
        print("STAGE 3: Generating video clips via Wan...")
        clip_paths = generate_all_clips(scene_prompts)
        print("Clips generated\n")

        # STAGE 4: Assemble
        print("STAGE 4: Assembling final video...")
        output_path = assemble_video(clip_paths)
        video_url = get_output_url(output_path)
        print("Assembly complete\n")

        return jsonify({
            "success": True,
            "topic": topic,
            "genre": genre,
            "vibe": vibe,
            "enriched_prompt": enriched_prompt,
            "script": script,
            "storyboard": scene_prompts,
            "bible": bible,
            "video_url": video_url,
            "scenes_count": len(scene_prompts)
        })

    except Exception as e:
        print(f"Pipeline error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# CONTINUATION VIDEO — edited/continued script + existing bible -> video.
# Reuses the locked bible so the new part matches the original character.
@app.route('/generate/from-script-video', methods=['POST'])
def generate_from_script_video():
    try:
        data = request.get_json()
        script = data.get('script', '').strip()
        existing_bible = data.get('bible', None)
        num_scenes = int(data.get('num_scenes', DEFAULT_SCENES))

        if not script:
            return jsonify({"error": "Script is required"}), 400

        print("\nCONTINUATION VIDEO REQUEST")

        # Storyboard reusing the locked bible
        storyboard = generate_storyboard(
            script, num_scenes=num_scenes, existing_bible=existing_bible
        )
        scene_prompts = storyboard["scenes"]
        bible = storyboard["bible"]

        if not scene_prompts:
            return jsonify({"error": "Storyboard produced no scenes"}), 500

        clip_paths = generate_all_clips(scene_prompts)
        output_path = assemble_video(clip_paths)
        video_url = get_output_url(output_path)

        return jsonify({
            "success": True,
            "script": script,
            "storyboard": scene_prompts,
            "bible": bible,
            "video_url": video_url,
            "scenes_count": len(scene_prompts)
        })

    except Exception as e:
        print(f"Continuation error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# PREVIEW — enrich + script + storyboard. FREE. No video.
@app.route('/generate/preview', methods=['POST'])
def generate_preview():
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        genre = data.get('genre', 'drama').strip()
        num_scenes = int(data.get('num_scenes', DEFAULT_SCENES))

        if not topic:
            return jsonify({"error": "Topic is required"}), 400

        enrichment = enrich_prompt(topic)
        enriched_prompt = enrichment["enriched"]
        vibe = enrichment["vibe"]

        script = generate_script(enriched_prompt, vibe=vibe, num_scenes=num_scenes)
        storyboard = generate_storyboard(script, num_scenes=num_scenes)
        scene_prompts = storyboard["scenes"]
        bible = storyboard["bible"]

        return jsonify({
            "success": True,
            "topic": topic,
            "genre": genre,
            "vibe": vibe,
            "enriched_prompt": enriched_prompt,
            "script": script,
            "storyboard": scene_prompts,
            "bible": bible,
            "scenes_count": len(scene_prompts)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# FROM-SCRIPT (text only) — rebuild storyboard from an edited/continued
# script, reusing bible. FREE. Used to preview a continuation before video.
@app.route('/generate/from-script', methods=['POST'])
def generate_from_script():
    try:
        data = request.get_json()
        script = data.get('script', '').strip()
        num_scenes = int(data.get('num_scenes', DEFAULT_SCENES))
        existing_bible = data.get('bible', None)

        if not script:
            return jsonify({"error": "Script is required"}), 400

        storyboard = generate_storyboard(
            script, num_scenes=num_scenes, existing_bible=existing_bible
        )
        scene_prompts = storyboard["scenes"]
        bible = storyboard["bible"]

        return jsonify({
            "success": True,
            "script": script,
            "storyboard": scene_prompts,
            "bible": bible,
            "scenes_count": len(scene_prompts)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT, host='0.0.0.0')