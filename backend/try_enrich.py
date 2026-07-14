from agents.enrichment_agent import enrich_prompt

while True:
    user_input = input("\nType your prompt (or 'quit' to stop): ")
    if user_input.lower() in ("quit", "exit", "q"):
        break
    result = enrich_prompt(user_input)
    print(f"\nVIBE:     {result['vibe']}")
    print(f"ENRICHED: {result['enriched']}")