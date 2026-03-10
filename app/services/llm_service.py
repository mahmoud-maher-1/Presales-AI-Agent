from app.services.gemini_service import GeminiService
from app.services.openrouter_service import OpenRouterService


def generate_ai_response(prompt: str) -> dict:
    # 1) Try Gemini first
    try:
        gemini = GeminiService()
        response = gemini.generate(prompt)

        print("[LLM] Provider: Gemini")

        return {
            "provider": "gemini",
            "text": response,
        }

    except Exception as e:
        print(f"[LLM] Gemini failed: {repr(e)}")

    # 2) Fallback to OpenRouter
    try:
        openrouter = OpenRouterService()
        response = openrouter.generate(prompt)

        print("[LLM] Provider: OpenRouter")

        return {
            "provider": "openrouter",
            "text": response,
        }

    except Exception as e:
        print(f"[LLM] OpenRouter failed: {repr(e)}")

        return {
            "provider": "none",
            "text": "عذرًا، خدمة الذكاء الاصطناعي غير متاحة حاليًا. حاول مرة أخرى بعد قليل.",
        }