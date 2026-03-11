from app.services.gemini_service import GeminiService
from app.services.openrouter_service import OpenRouterService
from app.services.grok_service import GrokService


def generate_ai_response(prompt: str) -> dict:
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

    try:
        grok = GrokService()
        response = grok.generate(prompt)
        print("[LLM] Provider: Grok")
        return {
            "provider": "grok",
            "text": response,
        }
    except Exception as e:
        print(f"[LLM] Grok failed: {repr(e)}")

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