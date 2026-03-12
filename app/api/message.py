from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.message_processor import process_message
from app.agent.summary_generator import generate_full_summary
from app.db.deps import get_db
from app.models.message import Message
from app.models.project_requirement import ProjectRequirement
from app.schemas.message import (
    MessageRequest,
    MessageResponse,
    ProjectSummaryResponse,
)

router = APIRouter()


@router.post("/message", response_model=MessageResponse)
def send_message(
    data: MessageRequest,
    db: Session = Depends(get_db)
):
    return process_message(db, data.customer_key, data.message)


@router.get(
    "/conversation/{conversation_id}/summary",
    response_model=ProjectSummaryResponse,
)
def get_project_summary(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    requirement = db.scalar(
        select(ProjectRequirement).where(
            ProjectRequirement.conversation_id == conversation_id
        )
    )

    if not requirement:
        raise HTTPException(status_code=404, detail="Summary not found")

    # Load conversation history for Kano analysis
    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id.asc())
    ).all()

    history = "\n".join(
        [f"{msg.role.value}: {msg.content}" for msg in messages]
    )

    result = generate_full_summary(requirement, history)

    return {
        "conversation_id": conversation_id,
        "summary": result["summary"],
        "kano_analysis": result["kano_analysis"],
    }