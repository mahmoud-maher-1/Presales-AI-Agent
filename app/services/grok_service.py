import httpx
from app.core.config import settings


class GrokService:
    def __init__(self):
        if not settings.GROK_API_KEY:
            raise ValueError("GROK_API_KEY is missing")

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {settings.GROK_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.GROK_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = httpx.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60.0,
        )

        print("[Grok] status:", response.status_code)
        print("[Grok] body:", response.text)

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]