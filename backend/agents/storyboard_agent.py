import os
import json
from openai import OpenAI
from config import DASHSCOPE_API_KEY, QWEN_MODEL

client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

STORYBOARD_SYSTEM_PROMPT = """
You are a film director and cinematographer planning a single
continuous short drama for a text-to-video AI (Wan).

GOAL: Every scene must look like it belongs to ONE continuous film —
same characters, same location, same visual world.

CRITICAL TECHNIQUE — ONE CHARACTER PER SHOT:
Text-to-video cannot reliably keep two consistent faces in the same
frame. So even when a scene has two people talking, you film it the
way real directors do: cut between single-character shots. Show one
person reacting, then cut to the other speaking. NEVER put two named
characters in the same shot. Each generated clip contains exactly one
person (or a hand / object / empty space), never two faces at once.

STEP 1 — Build a STORY BIBLE (locked, reused everywhere):
- CHARACTERS: For EVERY character in the script, give an exact,
  unchanging physical description — age, build, hair (color, length,
  style), skin tone, exact clothing with colors, one memorable
  feature. These descriptions are copied word-for-word into every
  shot that character appears in. Never vary them.
- LOCATION: One consistent place, described concretely.
- TIME & LIGHT: One time of day, one lighting style.
- PALETTE & MOOD: Consistent colors and emotional tone.

STEP 2 — Break the story into shots (not scenes). A two-person
exchange becomes multiple single-character shots that intercut.
Each shot:
- Opens with ONE character's exact bible description (or a hand/
  object/room if no face is needed)
- Uses the exact same location, light, and palette
- Adds shot type (close up / medium / wide) and one clear action
- Progresses the story: establish -> escalate -> payoff
- Ends with: cinematic, realistic, consistent film look

RULES:
- Exactly ONE named character per shot. Never two faces together.
- Keep every character visually identical across all their shots.
- No meta-notes, no bracketed instructions, no explanations inside
  the prompts — only pure visual description Wan can render.
- Each prompt is one flowing paragraph, rich in visual detail.

OUTPUT — return ONLY valid JSON, no markdown, no preamble:
{
  "bible": {
    "characters": ["desc of character 1", "desc of character 2"],
    "location": "...",
    "light": "...",
    "palette": "..."
  },
  "scenes": [
    "full wan prompt for shot 1 ...",
    "full wan prompt for shot 2 ...",
    "full wan prompt for shot 3 ..."
  ]
}
"""


def generate_storyboard(script: str, num_scenes: int = 3,
                        existing_bible: dict = None) -> dict:
    """
    Convert a script into continuity-locked, one-character-per-shot Wan
    prompts. If existing_bible is provided, new shots reuse that locked
    character/world so continued scenes match the original film.

    Args:
        script: The full drama script
        num_scenes: How many shots to produce
        existing_bible: Optional locked bible from a previous generation

    Returns:
        dict with 'scenes' (list of Wan prompts) and 'bible'
    """

    if existing_bible:
        bible_instruction = f"""
    IMPORTANT — This is a CONTINUATION. You MUST reuse this exact locked
    bible. Do NOT invent new characters, locations, or palettes. The
    continued shots must look identical in world and character to what
    came before:

    LOCKED BIBLE:
    {json.dumps(existing_bible, indent=2)}

    Use these exact character descriptions, location, light, and palette
    in the new shots, and return this same bible back in your output.
    """
    else:
        bible_instruction = ""

    user_prompt = f"""
    Turn this script into EXACTLY {num_scenes} shots following your
    instructions. {bible_instruction}
    Build (or reuse) the story bible, then break the story into
    single-character shots that intercut so the whole thing looks like
    one continuous film. Never place two named characters in the same shot.

    SCRIPT:
    {script}
    """

    try:
        response = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[
                {"role": "system", "content": STORYBOARD_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2000,
            temperature=0.4
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        # Strip em-dashes everywhere before parsing
        raw = raw.replace("\u2014", ",").replace("--", ",")

        data = json.loads(raw)
        scenes = data.get("scenes", [])[:num_scenes]
        bible = data.get("bible", existing_bible or {})

        if not scenes:
            raise Exception("No scenes produced")

        return {"scenes": scenes, "bible": bible}

    except json.JSONDecodeError:
        raise Exception(
            "Storyboard did not return valid JSON. Raw output:\n" + raw
        )
    except Exception as e:
        raise Exception(f"Storyboard generation failed: {str(e)}")


# Text-only test — costs zero video quota
if __name__ == "__main__":
    test_script = """
    SCENE 1:
    [Kitchen, morning]
    Lily picks up Jamal's phone. One message. Her face changes.

    SCENE 2:
    [Living room]
    Jamal walks in smiling. "You're up early." She doesn't move.

    SCENE 3:
    [Balcony, dusk]
    Lily takes off her ring, places it on the railing, walks away.
    """

    print("Generating storyboard...\n")
    result = generate_storyboard(test_script, num_scenes=3)
    print("BIBLE:", json.dumps(result["bible"], indent=2), "\n")
    for i, scene in enumerate(result["scenes"], 1):
        print(f"--- SHOT {i} ---")
        print(scene)
        print()