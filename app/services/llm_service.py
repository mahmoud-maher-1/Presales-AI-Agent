from app.services.gemini_service import GeminiService
from app.services.openrouter_service import OpenRouterService
from app.services.groq_service import GroqService


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
        groq = GroqService()
        response = groq.generate(prompt)
        print("[LLM] Provider: Groq")
        return {
            "provider": "groq",
            "text": response,
        }
    except Exception as e:
        print(f"[LLM] Groq failed: {repr(e)}")

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
        "text": "معلش، خدمة الذكاء الاصطناعي مش متاحة دلوقتي. جرب تاني بعد شوية.",
    }