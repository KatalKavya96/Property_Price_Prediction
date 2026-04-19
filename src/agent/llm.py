import os
import requests
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


@lru_cache(maxsize=50)
def get_llm_response(prompt: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-OpenRouter-Title": "Property Price Advisory Agent",
    }

    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a grounded real estate investment advisor. "
                    "Use only the provided prediction, comparable analysis, "
                    "and retrieved market context. Do not invent legal facts, "
                    "regulations, or guarantees."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.2,
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)

    if response.status_code != 200:
        try:
            error_payload = response.json()
        except Exception:
            error_payload = response.text
        raise ValueError(f"OpenRouter API error: {error_payload}")

    payload = response.json()

    if "choices" not in payload or not payload["choices"]:
        raise ValueError(f"Unexpected OpenRouter response: {payload}")

    message = payload["choices"][0].get("message", {})
    content = message.get("content", "")

    if not content or not content.strip():
        raise ValueError(f"OpenRouter returned blank content: {payload}")

    return content.strip()