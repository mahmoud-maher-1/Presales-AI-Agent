from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.agent.summary_generator import generate_full_summary
from app.db.deps import get_db
from app.models.message import Message
from app.models.project_requirement import ProjectRequirement

router = APIRouter()

@router.get("/conversation/{conversation_id}/summary")
def get_conversation_summary(
    conversation_id: int,
    lang: str = Query("en", pattern="^(en|ar)$"),
    db: Session = Depends(get_db),
):

    requirement = db.scalar(
        select(ProjectRequirement).where(
            ProjectRequirement.conversation_id == conversation_id
        )
    )

    if not requirement:
        return {
            "conversation_id": conversation_id,
            "summary": None,
            "kano_analysis": None,
            "srs_document": None,
        }

    # Load conversation history for Kano analysis & SRS generation
    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id.asc())
    ).all()

    history = "\n".join(
        [f"{msg.role.value}: {msg.content}" for msg in messages]
    )

    result = generate_full_summary(requirement, history, lang=lang)

    return {
        "conversation_id": conversation_id,
        "summary": result["summary"],
        "kano_analysis": result["kano_analysis"],
        "srs_document": result["srs_document"],
    }