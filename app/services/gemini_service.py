from google import genai
from google.genai import errors

from app.core.config import settings


class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing")
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )
            return response.text or "عذرًا، لم أتمكن من توليد رد الآن."
        except errors.ClientError as e:
            raise RuntimeError(f"GEMINI_ERROR: {str(e)}") from e
