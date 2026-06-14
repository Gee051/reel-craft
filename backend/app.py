import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add backend directory to path so agents can import config
sys.path.insert(0, os.path.dirname(__file__))

# Import all four agents
from agents.script_agent import generate_script
from agents.storyboard_agent import generate_storyboard
from agents.video_agent import generate_all_clips
from agents.assembly_agent import assemble_video, get_output_url

from config import DEBUG, PORT

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow React frontend to talk to Flask backend

# Serve generated videos to frontend
@app.route('/output/<filename>')
def serve_video(filename):
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    return send_from_directory(output_dir, filename)


# Health check — proves backend is running on Alibaba Cloud
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "running",
        "service": "Reel Craft API",
        "cloud": "Alibaba Cloud",
        "models": {
            "text": "qwen-plus",
            "video": "wanx2.1-t2v-plus (Wan)"
        }
    })


# Main pipeline endpoint
@app.route('/generate', methods=['POST'])
def generate():
    """
    Main pipeline — runs all four agents in sequence:
    1. Script Agent    → generates drama script
    2. Storyboard Agent → converts script to visual scenes
    3. Video Agent     → generates clips via Wan
    4. Assembly Agent  → stitches clips into final video
    """
    
    try:
        # Get input from frontend
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No data provided"
            }), 400
        
        topic = data.get('topic', '').strip()
        genre = data.get('genre', 'drama').strip()
        
        if not topic:
            return jsonify({
                "error": "Topic is required"
            }), 400
        
        print(f"\n{'='*50}")
        print(f"NEW GENERATION REQUEST")
        print(f"Topic: {topic}")
        print(f"Genre: {genre}")
        print(f"{'='*50}\n")
        
        # STAGE 1: Generate Script
        print("STAGE 1: Generating script...")
        script = generate_script(topic, genre)
        print(f"Script generated successfully\n")
        
        # STAGE 2: Generate Storyboard
        print("STAGE 2: Generating storyboard...")
        scene_prompts = generate_storyboard(script)
        print(f"Storyboard generated — {len(scene_prompts)} scenes\n")
        
        if not scene_prompts:
            return jsonify({
                "error": "Storyboard generation produced no scenes"
            }), 500
        
        # STAGE 3: Generate Video Clips via Wan
        print("STAGE 3: Generating video clips via Wan...")
        clip_paths = generate_all_clips(scene_prompts)
        print(f"All clips generated successfully\n")
        
        # STAGE 4: Assemble Final Video
        print("STAGE 4: Assembling final video...")
        output_path = assemble_video(clip_paths)
        video_url = get_output_url(output_path)
        print(f"Assembly complete\n")
        
        # Return success response to frontend
        return jsonify({
            "success": True,
            "topic": topic,
            "genre": genre,
            "script": script,
            "storyboard": scene_prompts,
            "video_url": video_url,
            "scenes_count": len(scene_prompts)
        })
    
    except Exception as e:
        print(f"Pipeline error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Script only endpoint — for testing script quality
@app.route('/generate/script', methods=['POST'])
def generate_script_only():
    """
    Generate just the script — useful for testing
    script quality before running full pipeline
    """
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        genre = data.get('genre', 'drama').strip()
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        script = generate_script(topic, genre)
        
        return jsonify({
            "success": True,
            "topic": topic,
            "script": script
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Storyboard only endpoint — for testing storyboard output
@app.route('/generate/storyboard', methods=['POST'])
def generate_storyboard_only():
    """
    Generate script + storyboard only — no video
    Useful for testing before spending video tokens
    """
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        genre = data.get('genre', 'drama').strip()
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        script = generate_script(topic, genre)
        scene_prompts = generate_storyboard(script)
        
        return jsonify({
            "success": True,
            "topic": topic,
            "script": script,
            "storyboard": scene_prompts
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(
        debug=DEBUG,
        port=PORT,
        host='0.0.0.0'
    )