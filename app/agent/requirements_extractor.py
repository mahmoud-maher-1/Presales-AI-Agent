import json
import logging

from app.agent.prompts import build_extraction_prompt
from app.services.llm_service import generate_ai_response

logger = logging.getLogger(__name__)


def _clean_json_text(text: str) -> str:
    cleaned = text.strip()

    if cleaned.startswith("```"):
        first_newline = cleaned.find("\n")
        if first_newline != -1:
            cleaned = cleaned[first_newline + 1:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    return cleaned.strip()


def extract_requirements(message: str, history: str | None = None) -> dict:
    prompt = build_extraction_prompt(message=message, history=history)

    result = generate_ai_response(prompt)
    text = result.get("text", "")
    provider = result.get("provider", "unknown")

    if not text.strip():
        logger.warning("Extractor returned empty text from provider=%s", provider)
        return {}

    try:
        cleaned = _clean_json_text(text)
        parsed = json.loads(cleaned)

        if not isinstance(parsed, dict):
            logger.warning("Extractor returned non-dict JSON from provider=%s", provider)
            return {}

        allowed_keys = {
            "project_type",
            "project_domain",
            "target_users",
            "platforms",
            "main_features",
            "timeline",
            "budget",
            "notes",
        }

        normalized = {key: parsed.get(key) for key in allowed_keys}

        return normalized

    except Exception:
        logger.warning(
            "Extractor failed to parse JSON from provider=%s. Raw text=%s",
            provider,
            text,
        )
        return {}