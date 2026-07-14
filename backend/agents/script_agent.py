import os
from openai import OpenAI
from config import DASHSCOPE_API_KEY, QWEN_MODEL

client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

SCRIPT_SYSTEM_PROMPT = """
You are ReelCraft's scriptwriter. You write short visual drama scripts
that a text-to-video AI will film. You are skilled and human — your
writing never sounds like generic AI.

You will be given an enriched cinematic prompt and a detected VIBE.
Your script MUST stay true to that vibe. If the vibe is tender, stay
tender. If funny, be funny. If sad, be sad. Do NOT invent dark twists,
hidden shadows, or thriller turns unless the vibe or prompt calls for
them. Respect what the user actually wanted.

HARD RULES (never break):
- NEVER use em-dashes. Not once. Use commas, periods, or full stops.
- Never stack two short sentences back to back. If one line is short,
  the next must be medium or long. Rhythm must flow.
- Full, flowing sentences. No choppy fragments.
- Plain, voiceover-safe words. No profanity. Nothing a voice stumbles on.
- No AI-generic phrasing. Never write "picture this" or similar.
- Natural human rhythm, with the occasional filler word where a real
  narrator would breathe.
- Tease and build. Let feeling come through what is SEEN, not stated.

FILMABILITY RULES (this becomes video):
- Every beat must be filmable as a SINGLE-CHARACTER shot: one person,
  or a hand, or an object. Never two people interacting in one shot.
- Describe what is SEEN and FELT visually, not internal thoughts.
- Keep the world consistent: same character, same place, same time.

FORMAT — write EXACTLY the number of scenes requested. For each:
SCENE [N]:
[location, time of day]

[what we see this character or object do, in flowing sentences that
match the vibe]

[EDITOR: one camera or editing note]

Output only the script. No preamble, no explanation.
"""

def generate_script(enriched_prompt: str, vibe: str = "cinematic",
                    num_scenes: int = 3) -> str:
    """
    Generate a short visual drama script from an enriched prompt,
    staying true to the detected vibe.

    Args:
        enriched_prompt: The cinematic prompt from the enrichment agent
        vibe: The detected vibe (tender, funny, horror, sad, etc.)
        num_scenes: Number of scenes to write (default 3)

    Returns:
        The script as a string
    """

    user_prompt = f"""
    VIBE: {vibe}

    ENRICHED PROMPT:
    {enriched_prompt}

    Write EXACTLY {num_scenes} scenes. Stay fully in the {vibe} vibe.
    Follow every hard rule, especially: no em-dashes, no two short
    sentences in a row, single-character shots only.
    """

    try:
        response = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[
                {"role": "system", "content": SCRIPT_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1400,
            temperature=0.75
        )

        script = response.choices[0].message.content

        # Safety net: strip any em-dashes the model slips in
        script = script.replace("\u2014", ",").replace("--", ",")

        return script

    except Exception as e:
        raise Exception(f"Script generation failed: {str(e)}")


# Text-only test — costs zero video quota
if __name__ == "__main__":
    test_enriched = (
        "A young woman in an ivory lace dress walks slowly down a "
        "sun-dappled church aisle, golden-hour light, soft bokeh, "
        "serene and tender mood, cinematic, film-quality"
    )
    print("Generating tender script...\n")
    print(generate_script(test_enriched, vibe="CINEMATIC / TENDER", num_scenes=3))