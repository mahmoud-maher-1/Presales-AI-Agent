from app.agent.missing_fields import (
    build_known_requirements,
    detect_missing_without_repetition,
)
from app.agent.prompts import build_next_question_prompt
from app.services.llm_service import generate_ai_response


def generate_next_question(requirement, history: str) -> tuple[str, list[str], str]:
    missing_fields, asked_topics = detect_missing_without_repetition(
        requirement=requirement,
        history=history,
    )

    if not missing_fields:
        return (
            "ممتاز، الصورة أصبحت أوضح الآن. هل تريد أن ألخص لك متطلبات المشروع الحالية بشكل منظم؟",
            [],
            "rule-based",
        )

    known = build_known_requirements(requirement)

    prompt = build_next_question_prompt(
        known=known,
        missing=missing_fields,
        asked_topics=asked_topics,
        history=history,
    )

    result = generate_ai_response(prompt)
    reply = result["text"].strip()

    if not reply:
        reply = "هل يمكنك توضيح المزيد عن المشروع؟"

    return reply, missing_fields, result["provider"]