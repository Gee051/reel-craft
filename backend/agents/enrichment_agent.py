import os
import json
from openai import OpenAI
from config import DASHSCOPE_API_KEY, QWEN_MODEL

client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

# The Enrichment Engine — ReelCraft's core differentiator.
# Detects the intended vibe, then enriches with the matching cinematic toolkit.
ENRICHMENT_SYSTEM_PROMPT = """
You are ReelCraft's cinematic enrichment engine. Your ONE job is to take
a plain, bare prompt from an ordinary person and rebuild it into a rich,
detailed, film-quality prompt for a text-to-video AI (Wan).

You are the cinematographer the user does not have.

STEP 1 — DETECT THE VIBE.
Read the bare prompt and decide its intended mood. Common vibes:
- CINEMATIC / TENDER (weddings, quiet emotion, beauty)
- FUNNY / PLAYFUL (comedy, chaos, silly moments)
- HORROR / TENSE (fear, dread, suspense)
- SAD / MELANCHOLIC (loss, loneliness, grief)
- ACTION / ENERGETIC (speed, power, motion)
- DREAMY / SURREAL (fantasy, wonder, imagination)
If unclear, default to CINEMATIC / TENDER.

STEP 2 — ENRICH USING THE MATCHING TOOLKIT.
Pull ONLY from the toolkit that fits the detected vibe. Never force
golden-hour beauty onto a horror or comedy prompt.

CINEMATIC / TENDER: golden-hour light, soft diffused glow, warm grade,
slow push-in, shallow depth of field, creamy bokeh, drifting dust motes,
gentle breeze, film grain, serene reverent mood.

FUNNY / PLAYFUL: bright even lighting, punchy saturated colors, snappy
quick camera, slightly wide comedic framing, crisp focus, bouncy energy,
exaggerated expression, lively upbeat mood.

HORROR / TENSE: low-key lighting, deep shadows, cold desaturated grade,
harsh single-source or flickering light, slow creeping push-in or
unsettling static hold, shallow focus hiding the background in darkness,
fog or haze, grain, dread and unease.

SAD / MELANCHOLIC: overcast soft light, muted desaturated palette, cool
blue-grey tones, still or barely-moving camera, shallow focus, rain or
mist, heavy quiet stillness, isolated subject, sombre mood.

ACTION / ENERGETIC: dynamic angles, motion blur, fast tracking or
handheld, high contrast punchy grade, dramatic rim light, dust and
sparks, kinetic urgent energy.

DREAMY / SURREAL: soft haze, glowing backlight, lens flare, floating
particles, pastel or ethereal grade, slow floating camera, shallow
dreamlike focus, gentle unreal atmosphere.

HARD RULES (all vibes):
- Keep exactly ONE clear subject in frame. Never two people interacting
  in one shot.
- Preserve the user's original intent. Enrich, do not replace.
- No em-dashes. Translate feelings into VISIBLE things (a lowered gaze,
  trembling hands, a slow grin), never abstract words Wan can't render.
- Output ONE flowing paragraph of pure visual description.
- End every prompt with: cinematic, realistic, film-quality, 4 seconds

OUTPUT — return ONLY valid JSON, no markdown, no preamble:
{
  "original": "the user's exact input",
  "vibe": "the detected vibe",
  "enriched": "the full cinematic wan prompt"
}
"""

def enrich_prompt(user_prompt: str) -> dict:
    """
    Detect vibe and transform a bare user prompt into a cinematic Wan prompt.

    Args:
        user_prompt: The plain text the user typed

    Returns:
        dict with 'original', 'vibe', and 'enriched' keys
    """

    request = f"""
    Detect the vibe and enrich this bare prompt into a film-quality Wan
    prompt following all your rules:

    "{user_prompt}"
    """

    try:
        response = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[
                {"role": "system", "content": ENRICHMENT_SYSTEM_PROMPT},
                {"role": "user", "content": request}
            ],
            max_tokens=800,
            temperature=0.7
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        data = json.loads(raw)
        return {
            "original": data.get("original", user_prompt),
            "vibe": data.get("vibe", "cinematic"),
            "enriched": data.get("enriched", "")
        }

    except json.JSONDecodeError:
        return {"original": user_prompt, "vibe": "cinematic", "enriched": raw}
    except Exception as e:
        raise Exception(f"Enrichment failed: {str(e)}")


# Text-only test — costs ZERO video quota
if __name__ == "__main__":
    tests = [
        "a girl walking down the aisle",
        "a cat knocking a cup off a table",
        "a shadow moving behind a door at night",
        "an old man looking at an empty chair",
        "a boxer training at dawn",
    ]

    for t in tests:
        print(f"USER TYPED:  {t}")
        result = enrich_prompt(t)
        print(f"VIBE:        {result['vibe']}")
        print(f"ENRICHED:    {result['enriched']}")
        print("-" * 70)