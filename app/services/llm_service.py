import logging
from typing import Optional

from app.services.gemini_service import GeminiService
from app.services.openrouter_service import OpenRouterService
from app.services.groq_service import GroqService

logger = logging.getLogger(__name__)


def _safe_call(provider_name: str, service, prompt: str) -> Optional[str]:
    """
    Safely call an LLM provider and return text or None if it fails.
    """
    try:
        response = service.generate(prompt)

        if not response or not str(response).strip():
            logger.warning(f"[LLM] {provider_name} returned empty response")
            return None

        logger.info(f"[LLM] Provider: {provider_name}")
        return str(response).strip()

    except Exception as e:
        logger.warning(f"[LLM] {provider_name} failed: {repr(e)}")
        return None


def generate_ai_response(prompt: str) -> dict:
    """
    Try multiple LLM providers in sequence until one succeeds.

    Order:
    1. OpenRouter
    2. Groq
    3. Gemini

    Returns:
        {
            "provider": "...",
            "text": "..."
        }
    """

    providers = [
        ("openrouter", OpenRouterService),
        ("groq", GroqService),
        ("gemini", GeminiService),
    ]

    for name, service_class in providers:
        try:
            service = service_class()
            result = _safe_call(name, service, prompt)

            if result:
                return {
                    "provider": name,
                    "text": result,
                }

        except Exception as e:
            logger.error(f"[LLM] Failed to initialize {name}: {repr(e)}")

    # fallback if all providers fail
    logger.error("[LLM] All providers failed")

    return {
        "provider": "none",
        "text": "معلش، خدمة الذكاء الاصطناعي غير متاحة حالياً. حاول مرة تانية بعد شوية.",
    }