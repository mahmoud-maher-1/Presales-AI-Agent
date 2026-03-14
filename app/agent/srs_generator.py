import json
import logging

from app.agent.prompts import build_srs_generation_prompt
from app.agent.summary_generator import generate_project_summary
from app.models.project_requirement import ProjectRequirement
from app.services.llm_service import generate_ai_response

logger = logging.getLogger(__name__)


def generate_srs(
    requirement: ProjectRequirement,
    history: str,
    lang: str = "en",
) -> dict | None:
    """
    Use LLM to generate a comprehensive SRS document from the conversation.

    Analyzes the full conversation history and extracted requirements to produce
    a structured, detailed SRS following IEEE 830 guidelines.

    Args:
        requirement: The ProjectRequirement ORM record.
        history: Full conversation history as a formatted string.
        lang: Language code — "en" (default) or "ar".

    Returns:
        A dict containing the structured SRS document, or None if LLM fails.
    """
    requirement_summary = generate_project_summary(requirement)

    prompt = build_srs_generation_prompt(
        requirement_summary=requirement_summary,
        history=history,
        lang=lang,
    )

    try:
        result = generate_ai_response(prompt)
        raw_text = result.get("text", "")

        # Strip markdown code fences if present
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            first_newline = cleaned.index("\n")
            cleaned = cleaned[first_newline + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        srs_data = json.loads(cleaned)

        # Validate expected structure
        if "sections" not in srs_data:
            logger.warning("SRS LLM response missing 'sections' key")
            return None

        return srs_data

    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Failed to parse SRS generation JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"SRS generation failed: {e}")
        return None
