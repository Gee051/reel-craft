import os
from openai import OpenAI
from config import DASHSCOPE_API_KEY, QWEN_MODEL

# Initialize Qwen client
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

# Storyboard system prompt — translates drama into visual language
STORYBOARD_SYSTEM_PROMPT = """
You are a professional cinematographer and storyboard artist 
specializing in short-form video content.

Your job is to read a short drama script and convert each 
scene into a precise visual description that a video 
generation AI can use to generate footage.

STRICT RULES:

1. ONE STORYBOARD ENTRY PER SCENE — each scene in the 
   script becomes exactly one visual description.

2. VISUAL LANGUAGE ONLY — describe what the camera sees.
   No dialogue. No internal thoughts. Only visuals.

3. EACH DESCRIPTION MUST INCLUDE:
   - Shot type (close up, wide shot, medium shot, etc.)
   - Subject and their physical state (posture, expression, action)
   - Environment (location, lighting, time of day)
   - Mood (tense, emotional, dramatic, suspenseful)
   - Duration in seconds (between 3-5 seconds)
   - Style (cinematic, realistic, dramatic lighting)

4. FORMAT — Use this exact structure for each scene:

   SCENE [NUMBER]:
   Shot: [shot type]
   Subject: [what/who is in frame and what they are doing]
   Environment: [location, lighting, atmosphere]
   Mood: [emotional tone]
   Duration: [X seconds]
   Style: cinematic, realistic, dramatic lighting
   
   Prompt: [one single flowing sentence combining all of 
   the above — this is what gets sent to the video model]

5. THE PROMPT LINE is the most important part. 
   It must be a single detailed sentence describing 
   the full visual in a way a video AI can understand.
   
   Example of a good prompt:
   "Close up shot of a young woman's trembling hands 
   holding a smartphone in a dimly lit kitchen, 
   shoulders tense, face turned away, cinematic 
   dramatic lighting, 4 seconds"

6. MAXIMUM 4 SCENES — match the number of scenes 
   in the script exactly.

Output only the storyboard. No explanations. No preamble.
"""

def generate_storyboard(script: str) -> list:
    """
    Convert a script into a list of visual scene descriptions
    optimized for Wan video generation.
    
    Args:
        script: The full drama script from script_agent
    
    Returns:
        List of scene prompt strings for Wan API
    """
    
    user_prompt = f"""
    Convert this script into a storyboard following 
    your exact instructions:
    
    {script}
    """
    
    try:
        response = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[
                {"role": "system", "content": STORYBOARD_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.5
        )
        
        storyboard_text = response.choices[0].message.content
        
        # Extract just the Prompt lines for Wan API
        scenes = []
        lines = storyboard_text.split('\n')
        
        for line in lines:
            if line.strip().startswith('Prompt:'):
                prompt = line.replace('Prompt:', '').strip()
                scenes.append(prompt)
        
        return scenes
    
    except Exception as e:
        raise Exception(f"Storyboard generation failed: {str(e)}")


# Test the agent directly
if __name__ == "__main__":
    # Sample script for testing
    test_script = """
    SCENE 1:
    [Kitchen, morning]
    She picks up his phone. One message. Her face changes.
    [EDITOR: Close up on eyes — hold 2 seconds]
    
    SCENE 2:
    [Living room]
    He walks in smiling. She doesn't move.
    "You're up early." She turns slowly.
    [EDITOR: Wide shot — slow zoom in on her face]
    """
    
    print("Generating storyboard...\n")
    scenes = generate_storyboard(test_script)
    
    for i, scene in enumerate(scenes, 1):
        print(f"Scene {i}: {scene}\n")