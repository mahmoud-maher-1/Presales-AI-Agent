from app.agent.missing_fields import (
    build_known_requirements,
    detect_missing_without_repetition,
)
from app.agent.prompts import build_next_question_prompt
from app.services.llm_service import generate_ai_response


def _has_value(value) -> bool:
    if value is None:
        return False

    if isinstance(value, str) and not value.strip():
        return False

    return True


def _detect_stage(known: dict, missing_fields: list[str]) -> str:
    core_ready = (
        _has_value(known.get("project_type"))
        and _has_value(known.get("project_domain"))
        and _has_value(known.get("target_users"))
        and _has_value(known.get("platforms"))
    )

    optional_count = 0
    for field in ["main_features", "timeline", "budget"]:
        if _has_value(known.get(field)):
            optional_count += 1

    if not missing_fields:
        return "closing"

    if core_ready and optional_count >= 1:
        return "closing"

    if core_ready:
        return "clarification"

    return "discovery"


def _fallback_reply(stage: str, missing_fields: list[str]) -> str:
    if stage == "closing":
        if "budget" in missing_fields:
            return "ممتاز، كده الصورة بقت واضحة جدًا. ممكن أعرف الميزانية المتوقعة أو الرينج المناسب للمشروع؟"

        if "timeline" in missing_fields:
            return "تمام جدًا. فاضل أعرف منك بس الوقت المتوقع اللي حابب المشروع يجهز فيه؟"

        return "كده عندنا تصور واضح جدًا. تحب ألخص متطلبات المشروع بشكل منظم، ولو مناسب تبعت رقم الموبايل علشان نرتب meeting؟"

    if stage == "clarification":
        return "ممتاز، كده فهمت الفكرة بشكل أحسن. ممكن توضحلي إيه أهم حاجة المستخدم هيعملها جوه النظام؟"

    return "ممكن توضحلي أكتر عن فكرة المشروع، ومين المستخدم الأساسي اللي هيستخدمه؟"


def generate_next_question(requirement, history: str) -> tuple[str, list[str], str]:
    missing_fields, asked_topics = detect_missing_without_repetition(
        requirement=requirement,
        history=history,
    )

    known = build_known_requirements(requirement)
    stage = _detect_stage(known, missing_fields)

    # لو الحوار اكتمل خلاص
    if stage == "closing" and not missing_fields:
        return (
            "ممتاز جدًا، كده الصورة بقت واضحة. تحب ألخصلك متطلبات المشروع بشكل منظم، ولو مناسب تبعت رقم الموبايل علشان نرتب meeting؟",
            [],
            "rule-based",
        )

    prompt = build_next_question_prompt(
        known=known,
        missing=missing_fields,
        asked_topics=asked_topics,
        history=history,
        stage=stage,
    )

    result = generate_ai_response(prompt)
    reply = result["text"].strip()

    if not reply:
        reply = _fallback_reply(stage, missing_fields)

    return reply, missing_fields, result["provider"]