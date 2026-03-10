from app.models.project_requirement import ProjectRequirement


FIELD_PRIORITY = [
    "project_type",
    "project_domain",
    "platforms",
    "target_users",
    "main_features",
    "timeline",
    "budget",
]


def is_missing(value) -> bool:
    if value is None:
        return True

    if isinstance(value, str) and not value.strip():
        return True

    return False

def detect_missing_fields(requirement: ProjectRequirement) -> list[str]:
    missing = []

    for field in FIELD_PRIORITY:
        value = getattr(requirement, field, None)
        if is_missing(value):
            missing.append(field)

    return missing


def build_known_requirements(requirement: ProjectRequirement) -> dict:
    return {
        "project_type": requirement.project_type,
        "project_domain": requirement.project_domain,
        "target_users": requirement.target_users,
        "platforms": requirement.platforms,
        "main_features": requirement.main_features,
        "timeline": requirement.timeline,
        "budget": requirement.budget,
    }


def extract_asked_topics(history: str) -> list[str]:
    text = history.lower()

    asked_topics = []

    topic_keywords = {
        "project_type": ["تطبيق", "موقع", "ويب", "system", "app", "website"],
        "project_domain": ["توصيل", "مطاعم", "متجر", "حجز", "تعليم", "عيادة", "طبي"],
        "platforms": ["android", "ios", "iphone", "منصة", "ويب", "لوحة تحكم"],
        "target_users": ["مستخدم", "عميل", "مندوب", "سائق", "إدارة", "admin"],
        "main_features": ["مميزات", "خصائص", "دفع", "تتبع", "إشعارات", "لوحة تحكم"],
        "timeline": ["مدة", "ميعاد", "وقت", "timeline", "جاهز", "شهر", "أسبوع"],
        "budget": ["ميزانية", "budget", "تكلفة", "سعر"],
    }

    for topic, keywords in topic_keywords.items():
        if any(keyword in text for keyword in keywords):
            asked_topics.append(topic)

    return asked_topics


def detect_missing_without_repetition(
    requirement: ProjectRequirement,
    history: str,
) -> tuple[list[str], list[str]]:
    missing = detect_missing_fields(requirement)
    asked_topics = extract_asked_topics(history)

    filtered_missing = [field for field in missing if field not in asked_topics]

    if not filtered_missing:
        filtered_missing = missing

    return filtered_missing, asked_topics