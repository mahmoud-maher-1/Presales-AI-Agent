import httpx
from app.core.config import settings


class GroqService:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing")

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.GROQ_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 8192,
        }

        response = httpx.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60.0,
        )

        print("[Groq] status:", response.status_code)
        print("[Groq] body:", response.text)

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]
