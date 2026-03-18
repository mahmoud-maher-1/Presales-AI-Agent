import json
import logging
import re
from typing import Optional

from app.agent.prompts import build_activity_diagram_prompt
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


def generate_activity_diagram(
    requirement: ProjectRequirement,
    history: str,
    lang: str = "ar",
) -> Optional[dict]:
    """
    Generate an activity diagram (Mermaid) from project requirements
    and conversation history.
    """

    raw_text = ""

    try:
        requirement_summary = generate_project_summary(requirement)

        prompt = build_activity_diagram_prompt(
            requirement_summary=requirement_summary,
            history=history,
            lang=lang,
        )

        result = generate_ai_response(prompt)

        if not result:
            logger.error("LLM returned no response for activity diagram")
            return None

        raw_text = result.get("text", "").strip()

        if not raw_text:
            logger.error("LLM returned empty activity diagram response")
            return None

        json_text = extract_json(raw_text)

        if not json_text:
            logger.error("Could not extract JSON from activity diagram response")
            logger.debug(f"Raw LLM response: {raw_text}")
            return None

        diagram_data = json.loads(json_text)

        # validation
        if not isinstance(diagram_data, dict):
            logger.error("Activity diagram JSON is not a dictionary")
            return None

        required_keys = {"title", "diagram_type", "mermaid", "steps"}

        if not required_keys.issubset(diagram_data.keys()):
            logger.warning("Activity diagram response missing required keys")
            return None

        if not isinstance(diagram_data.get("steps"), list):
            logger.warning("Activity diagram 'steps' field is not a list")
            return None

        if not isinstance(diagram_data.get("mermaid"), str):
            logger.warning("Activity diagram 'mermaid' field is not a string")
            return None

        return diagram_data

    except json.JSONDecodeError as e:
        logger.error(f"Activity diagram JSON parsing error: {e}")
        logger.debug(f"Raw LLM response: {raw_text}")
        return None

    except Exception as e:
        logger.exception(f"Activity diagram generation failed: {e}")
        return None