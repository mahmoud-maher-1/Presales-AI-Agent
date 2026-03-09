from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.conversation import Conversation, ConversationStatus
from app.models.message import Message, MessageRole
from app.services.ai_service import generate_reply


def process_message(db: Session, customer_key: str, message: str) -> dict:
    customer = db.scalar(select(Customer).where(Customer.external_key == customer_key))

    if not customer:
        customer = Customer(external_key=customer_key)
        db.add(customer)
        db.commit()
        db.refresh(customer)

    conversation = db.scalar(
        select(Conversation).where(
            Conversation.customer_id == customer.id,
            Conversation.status == ConversationStatus.OPEN,
        )
    )

    if not conversation:
        conversation = Conversation(customer_id=customer.id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    user_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=message,
    )
    db.add(user_message)

    agent_reply = generate_reply(message)

    assistant_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=agent_reply,
    )
    db.add(assistant_message)

    db.commit()

    return {
        "reply": agent_reply,
        "conversation_id": conversation.id,
    }
