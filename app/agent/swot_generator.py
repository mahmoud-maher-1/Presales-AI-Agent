import json
import logging
import re
from typing import Optional

from app.agent.prompts import build_swot_generation_prompt
from app.agent.summary_generator import generate_project_summary
from app.models.project_requirement import ProjectRequirement
from app.services.llm_service import generate_ai_response

logger = logging.getLogger(__name__)


def extract_json(text: str) -> Optional[str]:
    """
    Extract the first JSON object from an LLM response.
    Handles markdown fences and extra surrounding text.
    """
    if not text:
        return None

    text = text.strip()

    # remove markdown code fences
    text = re.sub(r"^```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    text = text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or start >= end:
        return None

    return text[start:end + 1]


def generate_swot(
    requirement: ProjectRequirement,
    history: str,
    lang: str = "ar",
) -> Optional[dict]:
    """
    Generate a SWOT analysis from project requirements and conversation history.
    """

    raw_text = ""

    try:
        requirement_summary = generate_project_summary(requirement)

        prompt = build_swot_generation_prompt(
            requirement_summary=requirement_summary,
            history=history,
            lang=lang,
        )

        result = generate_ai_response(prompt)

        if not result:
            logger.error("LLM returned no response for SWOT generation")
            return None

        raw_text = result.get("text", "").strip()

        if not raw_text:
            logger.error("LLM returned empty SWOT response")
            return None

        json_text = extract_json(raw_text)

        if not json_text:
            logger.error("Could not extract JSON from SWOT response")
            logger.debug(f"Raw LLM response: {raw_text}")
            return None

        swot_data = json.loads(json_text)

        # Validate structure
        required_keys = {
            "strengths",
            "weaknesses",
            "opportunities",
            "threats",
            "recommendation",
        }

        if not isinstance(swot_data, dict):
            logger.error("SWOT JSON is not a dictionary")
            return None

        if not required_keys.issubset(swot_data.keys()):
            logger.warning("SWOT LLM response missing required keys")
            return None

        # Optional: validate list fields
        for key in ["strengths", "weaknesses", "opportunities", "threats"]:
            if not isinstance(swot_data.get(key), list):
                logger.warning(f"SWOT field '{key}' is not a list")
                return None

        if not isinstance(swot_data.get("recommendation"), str):
            logger.warning("SWOT 'recommendation' field is not a string")
            return None

        return swot_data

    except json.JSONDecodeError as e:
        logger.error(f"SWOT JSON parsing error: {e}")
        logger.debug(f"Raw LLM response: {raw_text}")
        return None

    except Exception as e:
        logger.exception(f"SWOT generation failed: {e}")
        return None