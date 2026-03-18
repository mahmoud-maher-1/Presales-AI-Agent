import json
import logging
from typing import Any

from app.models.project import Project
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
    """
    if kano_data is None:
        return None

    try:
        suffix = f"_{lang}"
        opposite = "_ar" if lang == "en" else "_en"

        filtered_features = []
        for feature in kano_data.get("features", []):
            filtered = {
                "feature": feature.get(
                    f"feature{suffix}",
                    feature.get(f"feature{opposite}", ""),
                ),
                "category": feature.get("category", ""),
                "reason": feature.get(
                    f"reason{suffix}",
                    feature.get(f"reason{opposite}", ""),
                ),
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


def _to_json_text(data: dict | None) -> str | None:
    if data is None:
        return None
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"JSON serialization failed: {e}")
        return None


def _safe_str(value: Any, default: str = "N/A") -> str:
    if value is None:
        return default
    s = str(value).strip()
    return s if s else default


def _split_features(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]

    text = str(value).strip()
    if not text:
        return []

    return [item.strip() for item in text.split(",") if item.strip()]


def _fallback_activity_diagram(requirement: ProjectRequirement) -> dict:
    project_name = _safe_str(getattr(requirement, "project_type", None), "Project")
    main_features = _split_features(getattr(requirement, "main_features", None))

    steps = ["Open app", "Login"]
    if main_features:
        steps.extend(main_features[:3])
    else:
        steps.extend(["Use core feature", "Complete action"])
    steps.append("Receive confirmation")

    mermaid_lines = ["flowchart TD"]
    node_labels = [
        "Open App",
        "Login",
        *[feature.title() for feature in steps[2:-1]],
        "Receive Confirmation",
    ]

    node_ids = [chr(ord("A") + i) for i in range(len(node_labels))]

    for node_id, label in zip(node_ids, node_labels):
        mermaid_lines.append(f'{node_id}["{label}"]')

    for i in range(len(node_ids) - 1):
        mermaid_lines.append(f"{node_ids[i]} --> {node_ids[i + 1]}")

    return {
        "title": f"{project_name.title()} Activity Diagram",
        "steps": steps,
        "mermaid": "\n".join(mermaid_lines),
    }


def _normalize_activity_diagram(activity_diagram: Any, requirement: ProjectRequirement) -> dict:
    """
    Normalize activity diagram output to the structure expected by generate_activity_diagram_pdf().
    Expected:
    {
        "title": "...",
        "steps": [...],
        "mermaid": "flowchart TD ..."
    }
    """
    fallback = _fallback_activity_diagram(requirement)

    if activity_diagram is None:
        return fallback

    if isinstance(activity_diagram, str):
        text = activity_diagram.strip()

        # If it looks like Mermaid directly
        if "flowchart" in text or "graph " in text:
            return {
                "title": fallback["title"],
                "steps": fallback["steps"],
                "mermaid": text,
            }

        # Try to decode as JSON text
        try:
            parsed = json.loads(text)
            activity_diagram = parsed
        except Exception:
            return fallback

    if not isinstance(activity_diagram, dict):
        return fallback

    title = activity_diagram.get("title") or fallback["title"]
    steps = activity_diagram.get("steps")
    mermaid = activity_diagram.get("mermaid")

    if not isinstance(steps, list) or not steps:
        steps = fallback["steps"]
    else:
        steps = [str(step).strip() for step in steps if str(step).strip()]
        if not steps:
            steps = fallback["steps"]

    if not isinstance(mermaid, str) or not mermaid.strip():
        mermaid = fallback["mermaid"]

    return {
        "title": title,
        "steps": steps,
        "mermaid": mermaid,
    }


def generate_full_summary(
    requirement: ProjectRequirement,
    history: str,
    lang: str = "ar",
    customer_phone: str | None = None,
) -> dict:
    """
    Generate the complete project summary including:
    - basic summary
    - Kano Model analysis
    - SWOT analysis
    - Activity diagram
    - Lead score

    SRS intentionally removed.
    """
    from app.agent.activity_diagram_generator import generate_activity_diagram
    from app.agent.kano_classifier import classify_features_kano
    from app.agent.lead_scoring import calculate_lead_score

    summary = generate_project_summary(requirement)

    # Kano analysis
    raw_kano = classify_features_kano(requirement, history)
    kano_analysis = _filter_kano_by_lang(raw_kano, lang)

    if raw_kano is None:
        logger.warning("Kano classification returned None, summary will not include Kano data")

    # SWOT analysis
    swot_analysis = None
    try:
        from app.agent.swot_generator import generate_swot
        swot_analysis = generate_swot(requirement, history, lang)
    except ImportError:
        logger.info("SWOT generator not implemented yet, skipping SWOT analysis")
    except Exception as e:
        logger.warning(f"SWOT generation failed: {e}")

    # Activity diagram
    activity_diagram = None
    try:
        raw_activity = generate_activity_diagram(requirement, history, lang)
        activity_diagram = _normalize_activity_diagram(raw_activity, requirement)
    except ImportError:
        logger.info("Activity diagram generator not implemented yet, using fallback activity diagram")
        activity_diagram = _fallback_activity_diagram(requirement)
    except Exception as e:
        logger.warning(f"Activity diagram generation failed: {e}")
        activity_diagram = _fallback_activity_diagram(requirement)

    # Lead score
    lead_score = None
    try:
        lead_score = calculate_lead_score(
            requirement=requirement,
            history=history,
            customer_phone=customer_phone,
        )
    except Exception as e:
        logger.warning(f"Lead scoring failed: {e}")

    return {
        "summary": summary,
        "kano_analysis": kano_analysis,
        "swot_analysis": swot_analysis,
        "activity_diagram": activity_diagram,
        "lead_score": lead_score,
    }


def save_summary_outputs_to_project(
    project: Project,
    full_summary: dict,
) -> Project:
    """
    Save generated outputs into the Project record.
    """
    summary = full_summary.get("summary")
    kano_analysis = full_summary.get("kano_analysis")
    swot_analysis = full_summary.get("swot_analysis")
    activity_diagram = full_summary.get("activity_diagram")
    lead_score = full_summary.get("lead_score")

    project.summary = _to_json_text(summary)
    project.kano_analysis = _to_json_text(kano_analysis)
    project.swot_analysis = _to_json_text(swot_analysis)
    project.activity_diagram = _to_json_text(activity_diagram)

    # SRS intentionally removed
    project.srs_document = None

    if lead_score:
        project.lead_score = lead_score.get("score")
        project.lead_status = lead_score.get("status")

    return project