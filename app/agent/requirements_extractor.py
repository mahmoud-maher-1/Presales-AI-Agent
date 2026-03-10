import json

from app.agent.prompts import build_extraction_prompt
from app.services.llm_service import generate_ai_response


def extract_requirements(message: str, history: str | None = None) -> dict:
    prompt = build_extraction_prompt(message=message, history=history)

    result = generate_ai_response(prompt)
    text = result["text"]

    try:
        return json.loads(text)
    except Exception:
        print("[Extractor] Failed to parse JSON:", text)
        return {}