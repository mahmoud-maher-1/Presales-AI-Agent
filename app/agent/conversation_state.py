from app.models.project_requirement import ProjectRequirement


def has_value(value) -> bool:
    if value is None:
        return False

    if isinstance(value, str) and not value.strip():
        return False

    return True


def calculate_completion_score(requirement: ProjectRequirement) -> dict:
    fields = {
        "project_type": has_value(requirement.project_type),
        "project_domain": has_value(requirement.project_domain),
        "platforms": has_value(requirement.platforms),
        "target_users": has_value(requirement.target_users),
        "main_features": has_value(requirement.main_features),
        "timeline": has_value(requirement.timeline),
        "budget": has_value(requirement.budget),
    }

    score = sum(1 for value in fields.values() if value)
    total = len(fields)

    return {
        "score": score,
        "total": total,
        "fields": fields,
    }


def get_conversation_state(requirement: ProjectRequirement) -> dict:
    result = calculate_completion_score(requirement)
    score = result["score"]
    fields = result["fields"]

    core_ready = (
        fields["project_type"]
        and fields["project_domain"]
        and fields["target_users"]
        and fields["platforms"]
    )

    enough_for_summary = core_ready and (
        fields["main_features"] or fields["timeline"] or fields["budget"]
    )

    almost_ready_for_closing = core_ready and score >= 5

    if enough_for_summary:
        state = "ready_for_summary"
    elif almost_ready_for_closing:
        state = "ready_for_closing"
    elif score >= 2:
        state = "discovery_in_progress"
    else:
        state = "insufficient_information"

    return {
        "state": state,
        "score": score,
        "total": result["total"],
        "fields": fields,
        "core_ready": core_ready,
        "enough_for_summary": enough_for_summary,
        "almost_ready_for_closing": almost_ready_for_closing,
    }