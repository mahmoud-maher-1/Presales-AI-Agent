import httpx

from app.core.config import settings


class OpenRouterService:
    def __init__(self):
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is missing")

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://127.0.0.1:8000",
            "X-Title": "AI Tawasol",
        }

        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 8192,
        }

        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60.0,
        )

        print("[OpenRouter] status:", response.status_code)
        print("[OpenRouter] body:", response.text)

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]