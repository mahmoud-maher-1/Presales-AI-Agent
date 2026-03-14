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


def _filter_kano_by_lang(kano_data: dict | None, lang: str) -> dict | None:
    """
    Filter Kano analysis to show only the requested language fields.

    The Kano classifier always returns bilingual data (feature_en/feature_ar, etc.).
    This function selects the appropriate language keys for display.
    """
    if kano_data is None:
        return None

    try:
        suffix = f"_{lang}"
        opposite = "_ar" if lang == "en" else "_en"

        filtered_features = []
        for feature in kano_data.get("features", []):
            filtered = {
                "feature": feature.get(f"feature{suffix}", feature.get(f"feature{opposite}", "")),
                "category": feature.get("category", ""),
                "reason": feature.get(f"reason{suffix}", feature.get(f"reason{opposite}", "")),
            }
            filtered_features.append(filtered)

        return {
            "features": filtered_features,
            "strategic_recommendation": kano_data.get(
                f"strategic_recommendation{suffix}",
                kano_data.get(f"strategic_recommendation{opposite}", ""),
            ),
        }
    except Exception as e:
        logger.warning(f"Kano language filtering failed: {e}")
        return kano_data


def generate_full_summary(
    requirement: ProjectRequirement,
    history: str,
    lang: str = "en",
) -> dict:
    """
    Generate the complete project summary including Kano Model analysis
    and SRS document.

    Args:
        requirement: The ProjectRequirement ORM record.
        history: Full conversation history as a formatted string.
        lang: Language code — "en" (default) or "ar".

    Returns:
        {
            "summary": { ... basic requirement fields ... },
            "kano_analysis": { ... Kano classification (lang-filtered) ... } | None,
            "srs_document": { ... SRS document ... } | None,
        }
    """
    from app.agent.kano_classifier import classify_features_kano
    from app.agent.srs_generator import generate_srs

    summary = generate_project_summary(requirement)

    # Kano analysis — always generated bilingually, then filtered by lang
    raw_kano = classify_features_kano(requirement, history)
    kano_analysis = _filter_kano_by_lang(raw_kano, lang)

    if raw_kano is None:
        logger.warning("Kano classification returned None, summary will not include Kano data")

    # SRS document — generated in the requested language
    srs_document = generate_srs(requirement, history, lang)

    if srs_document is None:
        logger.warning("SRS generation returned None, summary will not include SRS data")

    return {
        "summary": summary,
        "kano_analysis": kano_analysis,
        "srs_document": srs_document,
    }