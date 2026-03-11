from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.conversation_state import get_conversation_state
from app.agent.presales_agent import PresalesAgent
from app.models.conversation import Conversation, ConversationStatus
from app.models.customer import Customer
from app.models.message import Message, MessageRole
from app.models.project_requirement import ProjectRequirement


def process_message(db: Session, customer_key: str, message: str) -> dict:
    # 1) find or create customer
    customer = db.scalar(
        select(Customer).where(Customer.external_key == customer_key)
    )

    if not customer:
        customer = Customer(external_key=customer_key)
        db.add(customer)
        db.commit()
        db.refresh(customer)

    # 2) find or create open conversation
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

    # 3) save user message
    user_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=message,
    )
    db.add(user_message)
    db.commit()

    # 4) load conversation history
    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.id.asc())
    ).all()

    history = "\n".join(
        [f"{msg.role.value}: {msg.content}" for msg in messages]
    )

    # 5) find or create requirement memory
    requirement_record = db.scalar(
        select(ProjectRequirement).where(
            ProjectRequirement.conversation_id == conversation.id
        )
    )

    if not requirement_record:
        requirement_record = ProjectRequirement(
            conversation_id=conversation.id
        )
        db.add(requirement_record)
        db.commit()
        db.refresh(requirement_record)

    # 6) run presales agent
    agent = PresalesAgent()
    requirements, agent_reply, missing_fields, provider = agent.run(
        message=message,
        history=history,
        requirement_record=requirement_record,
    )

    # 7) update requirement memory
    if requirements.get("project_type"):
        requirement_record.project_type = requirements["project_type"]

    if requirements.get("project_domain"):
        requirement_record.project_domain = requirements["project_domain"]

    if requirements.get("target_users"):
        requirement_record.target_users = requirements["target_users"]

    if requirements.get("platforms"):
        requirement_record.platforms = requirements["platforms"]

    if requirements.get("main_features"):
        requirement_record.main_features = requirements["main_features"]

    if requirements.get("timeline"):
        requirement_record.timeline = requirements["timeline"]

    if requirements.get("budget"):
        requirement_record.budget = requirements["budget"]

    if requirements:
        requirement_record.raw_extraction = str(requirements)

    db.commit()
    db.refresh(requirement_record)

    # 8) calculate updated conversation state
    state_info = get_conversation_state(requirement_record)

    # 9) save assistant message
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
        "provider": provider,
        "requirements": requirements,
        "missing_fields": missing_fields,
        "state": state_info["state"],
        "completion_score": state_info["score"],
    }