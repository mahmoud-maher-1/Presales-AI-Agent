from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
import io

from app.agent.conversation_state import get_conversation_state
from app.agent.kano_classifier import classify_features_kano
from app.agent.summary_generator import generate_project_summary, _filter_kano_by_lang
from app.agent.srs_generator import generate_srs
from app.db.deps import get_db
from app.models.message import Message
from app.models.project_requirement import ProjectRequirement
from app.services.pdf_generator import (
    generate_kano_pdf,
    generate_history_pdf,
    generate_srs_pdf,
)

router = APIRouter()


def _require_ready(requirement: ProjectRequirement):
    """Raise 400 if conversation is not ready for summary."""
    state_info = get_conversation_state(requirement)
    if state_info["state"] != "ready_for_summary":
        raise HTTPException(
            status_code=400,
            detail="Requirements are not yet complete. "
                   "The conversation must reach 'ready_for_summary' state before generating documents.",
        )


def _load_requirement_and_history(conversation_id: int, db: Session):
    """Load requirement record and conversation history."""
    requirement = db.scalar(
        select(ProjectRequirement).where(
            ProjectRequirement.conversation_id == conversation_id
        )
    )
    if not requirement:
        raise HTTPException(status_code=404, detail="No requirements found for this conversation.")

    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id.asc())
    ).all()

    history = "\n".join([f"{msg.role.value}: {msg.content}" for msg in messages])

    return requirement, messages, history


@router.get("/conversation/{conversation_id}/pdf/kano")
def download_kano_pdf(
    conversation_id: int,
    lang: str = Query("en", pattern="^(en|ar)$"),
    db: Session = Depends(get_db),
):
    requirement, messages, history = _load_requirement_and_history(conversation_id, db)
    _require_ready(requirement)

    raw_kano = classify_features_kano(requirement, history)
    if raw_kano is None:
        raise HTTPException(status_code=500, detail="Kano classification failed.")

    kano_filtered = _filter_kano_by_lang(raw_kano, lang)

    pdf_bytes = generate_kano_pdf(kano_filtered, lang)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="kano_analysis_{lang}.pdf"'},
    )


@router.get("/conversation/{conversation_id}/pdf/history")
def download_history_pdf(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    requirement, messages, history = _load_requirement_and_history(conversation_id, db)
    _require_ready(requirement)

    pdf_bytes = generate_history_pdf(messages)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="conversation_history.pdf"'},
    )


@router.get("/conversation/{conversation_id}/pdf/srs")
def download_srs_pdf(
    conversation_id: int,
    lang: str = Query("en", pattern="^(en|ar)$"),
    db: Session = Depends(get_db),
):
    requirement, messages, history = _load_requirement_and_history(conversation_id, db)
    _require_ready(requirement)

    srs_data = generate_srs(requirement, history, lang)
    if srs_data is None:
        raise HTTPException(status_code=500, detail="SRS generation failed.")

    pdf_bytes = generate_srs_pdf(srs_data, lang)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="srs_document_{lang}.pdf"'},
    )
