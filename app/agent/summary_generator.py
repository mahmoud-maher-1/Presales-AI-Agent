import logging

from app.models.project_requirement import ProjectRequirement

logger = logging.getLogger(__name__)


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


def generate_full_summary(
    requirement: ProjectRequirement,
    history: str,
) -> dict:
    """
    Generate the complete project summary including Kano Model analysis.

    Returns:
        {
            "summary": { ... basic requirement fields ... },
            "kano_analysis": { ... Kano classification ... } | None
        }
    """
    from app.agent.kano_classifier import classify_features_kano

    summary = generate_project_summary(requirement)

    kano_analysis = classify_features_kano(requirement, history)

    if kano_analysis is None:
        logger.warning("Kano classification returned None, summary will not include Kano data")

    return {
        "summary": summary,
        "kano_analysis": kano_analysis,
    }