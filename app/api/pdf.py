from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
import io

from app.agent.conversation_state import get_conversation_state
from app.agent.summary_generator import generate_full_summary
from app.agent.kano_classifier import classify_features_kano
from app.agent.summary_generator import _filter_kano_by_lang
from app.db.deps import get_db
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.message import Message
from app.models.project_requirement import ProjectRequirement
from app.services.pdf_generator import (
    generate_summary_pdf,
    generate_swot_pdf,
    generate_activity_diagram_pdf,
    generate_kano_pdf,
    generate_history_pdf,
)

router = APIRouter(tags=["pdf"])


def _require_ready(requirement: ProjectRequirement):
    """Raise 400 if conversation is not ready enough for document generation."""
    state_info = get_conversation_state(requirement)
    if state_info["state"] not in {"ready_for_summary", "ready_for_closing"}:
        raise HTTPException(
            status_code=400,
            detail=(
                "Requirements are not yet complete. "
                "The conversation must reach a near-complete state before generating documents."
            ),
        )


def _load_conversation_context(conversation_id: int, db: Session):
    """Load conversation, requirement, customer, messages, and serialized history."""
    conversation = db.scalar(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    requirement = db.scalar(
        select(ProjectRequirement).where(
            ProjectRequirement.conversation_id == conversation_id
        )
    )
    if not requirement:
        raise HTTPException(
            status_code=404,
            detail="No requirements found for this conversation.",
        )

    customer = db.scalar(
        select(Customer).where(Customer.id == conversation.customer_id)
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id.asc())
    ).all()

    history = "\n".join(
        [f"{msg.role.value}: {msg.content}" for msg in messages]
    )

    return conversation, requirement, customer, messages, history


@router.get("/conversation/{conversation_id}/pdf/summary")
def download_summary_pdf(
    conversation_id: int,
    lang: str = Query("en", pattern="^(en|ar)$"),
    db: Session = Depends(get_db),
):
    conversation, requirement, customer, messages, history = _load_conversation_context(
        conversation_id, db
    )
    _require_ready(requirement)

    full_summary = generate_full_summary(
        requirement=requirement,
        history=history,
        lang=lang,
        customer_phone=customer.phone,
    )

    pdf_bytes = generate_summary_pdf(
        summary_data=full_summary["summary"],
        lang=lang,
        conversation_id=conversation.id,
        customer_name=customer.name,
    )

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="summary_{conversation_id}_{lang}.pdf"'
        },
    )


@router.get("/conversation/{conversation_id}/pdf/swot")
def download_swot_pdf(
    conversation_id: int,
    lang: str = Query("en", pattern="^(en|ar)$"),
    db: Session = Depends(get_db),
):
    conversation, requirement, customer, messages, history = _load_conversation_context(
        conversation_id, db
    )
    _require_ready(requirement)

    full_summary = generate_full_summary(
        requirement=requirement,
        history=history,
        lang=lang,
        customer_phone=customer.phone,
    )

    swot_data = full_summary.get("swot_analysis")
    if swot_data is None:
        raise HTTPException(status_code=500, detail="SWOT generation failed.")

    pdf_bytes = generate_swot_pdf(
        swot_data=swot_data,
        lang=lang,
        conversation_id=conversation.id,
        customer_name=customer.name,
    )

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="swot_analysis_{conversation_id}_{lang}.pdf"'
        },
    )


@router.get("/conversation/{conversation_id}/pdf/activity")
def download_activity_diagram_pdf(
    conversation_id: int,
    lang: str = Query("en", pattern="^(en|ar)$"),
    db: Session = Depends(get_db),
):
    conversation, requirement, customer, messages, history = _load_conversation_context(
        conversation_id, db
    )
    _require_ready(requirement)

    full_summary = generate_full_summary(
        requirement=requirement,
        history=history,
        lang=lang,
        customer_phone=customer.phone,
    )

    activity_data = full_summary.get("activity_diagram")
    if activity_data is None:
        raise HTTPException(status_code=500, detail="Activity diagram generation failed.")

    pdf_bytes = generate_activity_diagram_pdf(
        activity_data=activity_data,
        lang=lang,
        conversation_id=conversation.id,
        customer_name=customer.name,
    )

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="activity_diagram_{conversation_id}_{lang}.pdf"'
        },
    )


@router.get("/conversation/{conversation_id}/pdf/kano")
def download_kano_pdf(
    conversation_id: int,
    lang: str = Query("en", pattern="^(en|ar)$"),
    db: Session = Depends(get_db),
):
    conversation, requirement, customer, messages, history = _load_conversation_context(
        conversation_id, db
    )
    _require_ready(requirement)

    raw_kano = classify_features_kano(requirement, history)
    if raw_kano is None:
        raise HTTPException(status_code=500, detail="Kano classification failed.")

    kano_filtered = _filter_kano_by_lang(raw_kano, lang)

    pdf_bytes = generate_kano_pdf(
        kano_data=kano_filtered,
        lang=lang,
        conversation_id=conversation.id,
        customer_name=customer.name,
    )

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="kano_analysis_{conversation_id}_{lang}.pdf"'
        },
    )


@router.get("/conversation/{conversation_id}/pdf/history")
def download_history_pdf(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    conversation, requirement, customer, messages, history = _load_conversation_context(
        conversation_id, db
    )
    _require_ready(requirement)

    pdf_bytes = generate_history_pdf(
        messages=messages,
        conversation_id=conversation.id,
        customer_name=customer.name,
    )

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="conversation_history_{conversation_id}.pdf"'
        },
    )