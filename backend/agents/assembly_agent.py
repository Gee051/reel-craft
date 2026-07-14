import os
import time
from moviepy import VideoFileClip, concatenate_videoclips


def assemble_video(clip_paths: list, output_filename: str = None) -> str:
    """
    Assemble individual scene clips into one final video.

    Args:
        clip_paths: List of local file paths for all clips in scene order
        output_filename: Name of the final output video (auto-generated if None)

    Returns:
        Local file path of the assembled final video
    """
    if output_filename is None:
        output_filename = f"reelcraft_{int(time.time())}.mp4"

    print("Starting video assembly...")
    print(f"Assembling {len(clip_paths)} clips...\n")

    # Validate all clips exist before starting
    for path in clip_paths:
        if not os.path.exists(path):
            raise Exception(f"Clip not found: {path}")

    try:
        # Load all clips
        clips = []
        for i, path in enumerate(clip_paths, 1):
            print(f"Loading scene {i}: {path}")
            clip = VideoFileClip(path)
            clips.append(clip)

        print("\nConcatenating clips...")

        # Stitch all clips together in sequence
        final_clip = concatenate_videoclips(clips, method="compose")

        # Create output directory if it doesn't exist
        output_dir = os.path.join(
            os.path.dirname(__file__), '..', 'output'
        )
        os.makedirs(output_dir, exist_ok=True)

        # Output file path
        output_path = os.path.join(output_dir, output_filename)

        print(f"Rendering final video to: {output_path}")

        # Write final video
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp_audio.m4a",
            remove_temp=True,
            logger=None
        )

        # Close all clips to free memory
        for clip in clips:
            clip.close()
        final_clip.close()

        print(f"\nFinal video assembled successfully!")
        print(f"Output: {output_path}")

        return output_path

    except Exception as e:
        raise Exception(f"Assembly failed: {str(e)}")


def get_output_url(output_path: str) -> str:
    """
    Convert local output path to a URL the frontend can access.

    Args:
        output_path: Local file path of assembled video

    Returns:
        Relative URL string for frontend
    """
    filename = os.path.basename(output_path)
    return f"/output/{filename}"


# Test the agent directly
if __name__ == "__main__":
    test_clips = [
        "clips/scene_1.mp4",
        "clips/scene_2.mp4",
    ]

    print("Testing assembly...\n")
    output = assemble_video(test_clips)
    print(f"Assembly complete: {output}")