import json
import logging

from app.agent.prompts import build_kano_classification_prompt
from app.agent.summary_generator import generate_project_summary
from app.models.project_requirement import ProjectRequirement
from app.services.llm_service import generate_ai_response

logger = logging.getLogger(__name__)


def classify_features_kano(
    requirement: ProjectRequirement,
    history: str,
) -> dict | None:
    """
    Use LLM to classify features from the conversation into Kano Model categories.

    Analyzes the full conversation history (not just the stored main_features field)
    to identify individual features and classify them based on the client's tone,
    urgency, and emphasis.

    Returns a dict with bilingual (EN/AR) Kano analysis, or None if LLM fails.
    """
    requirement_summary = generate_project_summary(requirement)

    prompt = build_kano_classification_prompt(
        requirement_summary=requirement_summary,
        history=history,
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

        kano_data = json.loads(cleaned)

        # Validate expected structure
        if "features" not in kano_data:
            logger.warning("Kano LLM response missing 'features' key")
            return None

        return kano_data

    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Failed to parse Kano classification JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"Kano classification failed: {e}")
        return None
