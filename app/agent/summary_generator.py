from app.models.project_requirement import ProjectRequirement


def generate_project_summary(requirement: ProjectRequirement) -> dict:
    return {
        "project_type": requirement.project_type,
        "project_domain": requirement.project_domain,
        "target_users": requirement.target_users,
        "platforms": requirement.platforms,
        "main_features": requirement.main_features,
        "timeline": requirement.timeline,
        "budget": requirement.budget,
        "notes": requirement.notes,
    }