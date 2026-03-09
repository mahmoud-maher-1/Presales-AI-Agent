from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.message import MessageRequest, MessageResponse
from app.services.message_processor import process_message

router = APIRouter()


@router.post("/message", response_model=MessageResponse)
def create_message(payload: MessageRequest, db: Session = Depends(get_db)):
    result = process_message(
        db=db,
        customer_key=payload.customer_key,
        message=payload.message,
    )
    return result
