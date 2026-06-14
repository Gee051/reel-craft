import os
from openai import OpenAI
from config import DASHSCOPE_API_KEY, QWEN_MODEL

# Initialize Qwen client using OpenAI-compatible format
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    )

# Your craft rules — this is the engine of Reelcraft
SCRIPT_SYSTEM_PROMPT = """
You are a professional short drama scriptwriter specializing 
in YouTube and short-form video content.

STRICT RULES YOU MUST FOLLOW:

1. HOOK — The very first line must drop the audience into 
   tension immediately. No setup. No introduction. 
   Start in the middle of something happening.

2. PAYOFF TEASE — Never reveal the payoff early. 
   Make the audience feel something is about to happen 
   without showing what it is yet.

3. SCENE ENDINGS — Every scene must end on an unresolved 
   beat that pulls the viewer into the next scene.

4. DIALOGUE — Must sound like real people talking. 
   Use interruptions, short sentences, reactions, 
   and incomplete thoughts. Never sound like an actor 
   reading lines.

5. PACING STRUCTURE:
   - Scene 1: Fast — establish tension immediately
   - Scene 2: Fast — escalate the tension
   - Scene 3: Slow — emotional peak moment
   - Scene 4: Payoff — the hit lands

6. EDITOR NOTES — After every scene include an editor 
   note in brackets like this:
   [EDITOR: Close up on her face — hold 2 seconds before cut]

7. FORMAT — Use this exact structure for each scene:
   SCENE [NUMBER]:
   [Location and time of day]
   
   [Character dialogue and action]
   
   [EDITOR: camera/editing instruction]

8. LENGTH — Maximum 4 scenes. Each scene maximum 
   5 lines of dialogue. Total script must work as 
   a 60-90 second short drama.

Output only the script. No explanations. No preamble.
"""

def generate_script(topic: str, genre: str = "drama") -> str:
    """
    Generate a short drama script based on topic and genre.
    
    Args:
        topic: What the drama is about
        genre: Type of drama (default: drama)
    
    Returns:
        Complete formatted script as string
    """
    
    user_prompt = f"""
    Write a short drama script about: {topic}
    Genre: {genre}
    
    Follow all the rules in your instructions exactly.
    """
    
    try:
        response = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[
                {"role": "system", "content": SCRIPT_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.8
        )
        
        script = response.choices[0].message.content
        return script
    
    except Exception as e:
        raise Exception(f"Script generation failed: {str(e)}")


# Test the agent directly
if __name__ == "__main__":
    test_topic = "a girl who discovers her boyfriend has a secret family"
    print("Generating script...\n")
    script = generate_script(test_topic)
    print(script)