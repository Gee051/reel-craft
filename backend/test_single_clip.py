from agents.video_agent import generate_video_clip

# Test ONE single scene only — protects coupon
test_prompt = (
    "Close up shot of a woman's eyes widening with quiet "
    "shock in a softly lit kitchen bathed in morning light, "
    "shallow focus, cinematic realistic style with dramatic "
    "natural lighting, 4 seconds"
)

print("Testing single video clip generation...")
print("This costs roughly $0.50\n")

clip_path = generate_video_clip(test_prompt, 1)
print(f"\nSuccess! Clip saved to: {clip_path}")