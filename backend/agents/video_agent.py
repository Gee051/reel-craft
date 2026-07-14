import os
import time
import requests
import dashscope
from dashscope import VideoSynthesis
from http import HTTPStatus
from config import DASHSCOPE_API_KEY, WAN_MODEL, VIDEO_SIZE, VIDEO_DURATION

# Set API key and international base URL
dashscope.api_key = DASHSCOPE_API_KEY
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'


def generate_video_clip(scene_prompt: str, scene_number: int) -> str:
    print(f"Generating video for scene {scene_number}...")
    print(f"Prompt: {scene_prompt}\n")
    try:
        response = VideoSynthesis.async_call(
            model=WAN_MODEL,
            prompt=scene_prompt,
            size=VIDEO_SIZE,
        )
        if response.status_code != HTTPStatus.OK:
            raise Exception(f"Wan API error: {response.message}")
        task_id = response.output.task_id
        print(f"Task submitted. Task ID: {task_id}")
        video_url = poll_for_video(task_id)
        clip_path = download_clip(video_url, scene_number)
        return clip_path
    except Exception as e:
        raise Exception(
            f"Video generation failed for scene {scene_number}: {str(e)}"
        )


def poll_for_video(task_id: str) -> str:
    max_attempts = 40
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        print(f"Checking status... attempt {attempt}/{max_attempts}")
        time.sleep(15)
        status_response = VideoSynthesis.fetch(task_id)
        task_status = status_response.output.task_status
        print(f"Status: {task_status}")
        if task_status == "SUCCEEDED":
            video_url = status_response.output.video_url
            print(f"Video ready: {video_url}\n")
            return video_url
        elif task_status == "FAILED":
            print("FULL FAILURE RESPONSE:")
            print(status_response)
            code = getattr(status_response.output, 'code', 'unknown')
            msg = getattr(status_response.output, 'message', 'no message')
            raise Exception(f"Wan task failed — code: {code}, message: {msg}")
        elif task_status in ["PENDING", "RUNNING"]:
            continue
    raise Exception("Video generation timed out after 10 minutes")


def download_clip(video_url: str, scene_number: int) -> str:
    clips_dir = os.path.join(
        os.path.dirname(__file__), '..', 'clips'
    )
    os.makedirs(clips_dir, exist_ok=True)
    clip_path = os.path.join(clips_dir, f"scene_{scene_number}.mp4")
    print(f"Downloading scene {scene_number}...")
    response = requests.get(video_url, stream=True)
    with open(clip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Scene {scene_number} saved to {clip_path}\n")
    return clip_path


def generate_all_clips(scene_prompts: list) -> list:
    clip_paths = []
    for i, prompt in enumerate(scene_prompts, 1):
        clip_path = generate_video_clip(prompt, i)
        clip_paths.append(clip_path)
    print(f"All {len(clip_paths)} clips generated successfully")
    return clip_paths