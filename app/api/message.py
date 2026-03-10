from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.message import MessageRequest
from app.agent.message_processor import process_message

router = APIRouter()


@router.post("/message")
def send_message(data: MessageRequest, db: Session = Depends(get_db)):
    return process_message(db, data.customer_key, data.message)