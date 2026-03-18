from app.models.project_requirement import ProjectRequirement


def _has_value(value) -> bool:
    if value is None:
        return False

    if isinstance(value, str) and not value.strip():
        return False

    return True


def calculate_lead_score(
    requirement: ProjectRequirement,
    history: str = "",
    customer_phone: str | None = None,
) -> dict:
    """
    تقييم مدى جدية العميل بناءً على المعلومات التي ذكرها أثناء المحادثة.
    """

    signals = {
        "project_type": _has_value(requirement.project_type),
        "project_domain": _has_value(requirement.project_domain),
        "target_users": _has_value(requirement.target_users),
        "platforms": _has_value(requirement.platforms),
        "main_features": _has_value(requirement.main_features),
        "timeline": _has_value(requirement.timeline),
        "budget": _has_value(requirement.budget),
        "phone_provided": _has_value(customer_phone),
        "meeting_intent": False,
        "long_conversation": False,
    }

    text = (history or "").lower()

    meeting_keywords = [
        "اجتماع",
        "مكالمة",
        "نتواصل",
        "نتكلم",
        "ميعاد",
        "متى يمكن",
        "اتصل",
        "اتواصل",
        "call",
        "meeting",
        "zoom",
    ]

    if any(keyword in text for keyword in meeting_keywords):
        signals["meeting_intent"] = True

    turn_count = 0
    if history:
        turn_count += history.count("USER:")
        turn_count += history.count("ASSISTANT:")

    if turn_count >= 6:
        signals["long_conversation"] = True

    score = 0

    # إشارات أساسية
    if signals["project_type"]:
        score += 10
    if signals["project_domain"]:
        score += 10
    if signals["target_users"]:
        score += 10
    if signals["platforms"]:
        score += 10

    # إشارات جدية قوية
    if signals["main_features"]:
        score += 15
    if signals["timeline"]:
        score += 15
    if signals["budget"]:
        score += 15

    # إشارات التحويل
    if signals["phone_provided"]:
        score += 10
    if signals["meeting_intent"]:
        score += 10
    if signals["long_conversation"]:
        score += 5

    score = max(0, min(score, 100))

    if score >= 80:
        status = "hot"
    elif score >= 55:
        status = "warm"
    else:
        status = "cold"

    return {
        "score": score,
        "status": status,
        "signals": signals,
    }