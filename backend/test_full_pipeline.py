import requests

print("Testing FULL pipeline — this costs ~$2 and takes 5-15 minutes\n")

response = requests.post(
    "http://localhost:5000/generate",
    json={
        "topic": "a woman realizes her sister has been reading her diary",
        "genre": "drama"
    },
    timeout=1200  # 20 minute timeout
)

data = response.json()

if data.get("success"):
    print("\n✅ FULL PIPELINE SUCCESS")
    print(f"Scenes: {data['scenes_count']}")
    print(f"Video URL: {data['video_url']}")
    print(f"\nScript preview:\n{data['script'][:300]}...")
else:
    print(f"\n❌ FAILED: {data.get('error')}")