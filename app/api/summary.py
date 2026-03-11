from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.deps import get_db
from app.models.project_requirement import ProjectRequirement

router = APIRouter()

@router.get("/conversation/{conversation_id}/summary")
def get_conversation_summary(conversation_id: int, db: Session = Depends(get_db)):

    requirement = db.scalar(
        select(ProjectRequirement).where(
            ProjectRequirement.conversation_id == conversation_id
        )
    )

    if not requirement:
        return {
            "conversation_id": conversation_id,
            "summary": None
        }

    return {
        "conversation_id": conversation_id,
        "summary": {
            "project_type": requirement.project_type,
            "project_domain": requirement.project_domain,
            "target_users": requirement.target_users,
            "platforms": requirement.platforms,
            "main_features": requirement.main_features,
            "timeline": requirement.timeline,
            "budget": requirement.budget,
            "notes": requirement.notes
        }
    }