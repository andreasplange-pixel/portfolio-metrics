#!/usr/bin/env python3
import anthropic, json, os, sys

client = anthropic.Anthropic(api_key=os.environ.get("CLAUDE_API_KEY"))

print("🔄 Fetching live metrics...")

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": """Run the extraetf-live-dashboard skill to get live 5-year metrics.

Output ONLY valid JSON:
{
  "assets": {
    "tech": {"return": X, "volatility": Y},
    "em": {"return": X, "volatility": Y},
    "ai": {"return": X, "volatility": Y},
    "core": {"return": X, "volatility": Y},
    "qual": {"return": X, "volatility": Y},
    "gold": {"return": X, "volatility": Y}
  },
  "correlation": {...},
  "source": "scalable_capital_5yr_computed",
  "timestamp": "ISO8601_TIMESTAMP"
}

Return ONLY JSON."""
    }]
)

try:
    data = json.loads(message.content[0].text.strip())
    with open("dashboard-metrics.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ Metrics saved")
except json.JSONDecodeError as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
