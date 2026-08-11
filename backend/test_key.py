import os
import requests
from dotenv import load_dotenv

load_dotenv()

resp = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    },
    json={
        "model": "claude-sonnet-4-5",
        "max_tokens": 50,
        "messages": [{"role": "user", "content": "Say OK"}],
    },
    timeout=30,
)

print("STATUS:", resp.status_code)
print(resp.text)