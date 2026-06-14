import os
import time
import requests
import dashscope
from dashscope.video.generation import VideoSynthesis
from config import DASHSCOPE_API_KEY, WAN_MODEL, VIDEO_SIZE, VIDEO_DURATION

# Set DashScope API key
dashscope.api_key = DASHSCOPE_API_KEY


def generate_video_clip(scene_prompt: str, scene_number: int) -> str:
    """
    Generate a single video clip from a scene description using Wan.
    
    Args:
        scene_prompt: Visual description from storyboard agent
        scene_number: Scene number for file naming
    
    Returns:
        Local file path of downloaded video clip
    """
    
    print(f"Generating video for scene {scene_number}...")
    print(f"Prompt: {scene_prompt}\n")
    
    try:
        # Submit video generation task to Wan
        response = VideoSynthesis.call(
            model=WAN_MODEL,
            prompt=scene_prompt,
            size=VIDEO_SIZE,
            duration=VIDEO_DURATION
        )
        
        # Check if task was submitted successfully
        if response.status_code != 200:
            raise Exception(
                f"Wan API error: {response.message}"
            )
        
        task_id = response.output.task_id
        print(f"Task submitted. Task ID: {task_id}")
        print("Waiting for video generation...")
        
        # Poll until video is ready
        # Wan takes several minutes — we check every 15 seconds
        video_url = poll_for_video(task_id)
        
        # Download the video clip locally
        clip_path = download_clip(video_url, scene_number)
        
        return clip_path
    
    except Exception as e:
        raise Exception(f"Video generation failed for scene "
                       f"{scene_number}: {str(e)}")


def poll_for_video(task_id: str) -> str:
    """
    Poll Wan API until video generation is complete.
    
    Args:
        task_id: The task ID returned by Wan
    
    Returns:
        URL of the generated video
    """
    
    max_attempts = 40  # 40 attempts x 15 seconds = 10 minutes max
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        
        # Wait 15 seconds between checks
        print(f"Checking status... attempt {attempt}/{max_attempts}")
        time.sleep(15)
        
        # Check task status
        status_response = VideoSynthesis.fetch(task_id)
        
        task_status = status_response.output.task_status
        print(f"Status: {task_status}")
        
        if task_status == "SUCCEEDED":
            video_url = status_response.output.video_url
            print(f"Video ready: {video_url}\n")
            return video_url
        
        elif task_status == "FAILED":
            raise Exception(
                f"Wan task failed: {status_response.message}"
            )
        
        # PENDING or RUNNING — keep waiting
        elif task_status in ["PENDING", "RUNNING"]:
            continue
    
    raise Exception("Video generation timed out after 10 minutes")


def download_clip(video_url: str, scene_number: int) -> str:
    """
    Download generated video clip to local storage.
    
    Args:
        video_url: Temporary URL from Wan API
        scene_number: Used for file naming
    
    Returns:
        Local file path of saved clip
    """
    
    # Create clips directory if it doesn't exist
    clips_dir = os.path.join(
        os.path.dirname(__file__), '..', 'clips'
    )
    os.makedirs(clips_dir, exist_ok=True)
    
    # File path for this clip
    clip_path = os.path.join(
        clips_dir, f"scene_{scene_number}.mp4"
    )
    
    # Download the video
    print(f"Downloading scene {scene_number}...")
    response = requests.get(video_url, stream=True)
    
    with open(clip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Scene {scene_number} saved to {clip_path}\n")
    return clip_path


def generate_all_clips(scene_prompts: list) -> list:
    """
    Generate video clips for all scenes.
    
    Args:
        scene_prompts: List of visual descriptions from 
                       storyboard agent
    
    Returns:
        List of local file paths for all clips
    """
    
    clip_paths = []
    
    for i, prompt in enumerate(scene_prompts, 1):
        clip_path = generate_video_clip(prompt, i)
        clip_paths.append(clip_path)
    
    print(f"All {len(clip_paths)} clips generated successfully")
    return clip_paths


# Test the agent directly
if __name__ == "__main__":
    test_prompts = [
        "Close up shot of a young woman's trembling hands "
        "holding a smartphone in a dimly lit kitchen, "
        "shoulders tense, cinematic dramatic lighting, "
        "4 seconds"
    ]
    
    print("Testing video generation...\n")
    clips = generate_all_clips(test_prompts)
    print(f"Generated clips: {clips}")