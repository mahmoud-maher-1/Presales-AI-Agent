from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.conversation_state import get_conversation_state
from app.agent.lead_scoring import calculate_lead_score
from app.agent.presales_agent import PresalesAgent

from app.models.conversation import Conversation, ConversationStatus
from app.models.customer import Customer
from app.models.message import Message, MessageRole
from app.models.project import Project, ProjectStatus
from app.models.project_requirement import ProjectRequirement


def _to_str(val):
    """Convert extracted values into strings suitable for DB text fields."""
    if val is None:
        return None
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        return ", ".join(str(item) for item in val)
    if isinstance(val, dict):
        import json
        return json.dumps(val, ensure_ascii=False)
    return str(val)


def _extract_phone(message: str) -> str | None:
    """
    Try to extract a phone number from the user message.
    Very simple version for now.
    """
    if not message:
        return None

    if not any(char.isdigit() for char in message):
        return None

    digits_only = "".join(
        ch for ch in message if ch.isdigit() or ch == "+"
    )

    if len(digits_only.replace("+", "")) >= 8:
        return digits_only

    return None


def process_message(db: Session, customer_key: str, message: str) -> dict:
    """
    Main entry point for processing chat messages.
    Handles customer, conversation, project, requirements,
    AI reply generation, and lead scoring.
    """

    # ─────────────────────────────────
    # 1️⃣ Find or create customer
    # ─────────────────────────────────

    customer = db.scalar(
        select(Customer).where(Customer.external_key == customer_key)
    )

    if not customer:
        customer = Customer(external_key=customer_key)
        db.add(customer)
        db.commit()
        db.refresh(customer)

    # ─────────────────────────────────
    # 2️⃣ Find or create open conversation
    # ─────────────────────────────────

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

    # ─────────────────────────────────
    # 3️⃣ Ensure conversation has project
    # ─────────────────────────────────

    project = None

    if conversation.project_id:
        project = db.scalar(
            select(Project).where(Project.id == conversation.project_id)
        )

    if not project:
        project = Project(
            customer_id=customer.id,
            name="Untitled Project",
            status=ProjectStatus.DISCOVERY,
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        conversation.project_id = project.id
        db.commit()
        db.refresh(conversation)

    # ─────────────────────────────────
    # 4️⃣ Save user message
    # ─────────────────────────────────

    user_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=message,
    )

    db.add(user_message)
    db.commit()

    # ─────────────────────────────────
    # 5️⃣ Load conversation history
    # ─────────────────────────────────

    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.id.asc())
    ).all()

    history = "\n".join(
        [f"{msg.role.value}: {msg.content}" for msg in messages]
    )

    # ─────────────────────────────────
    # 6️⃣ Find or create requirement memory
    # ─────────────────────────────────

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

    # ─────────────────────────────────
    # 7️⃣ Run presales agent
    # ─────────────────────────────────

    agent = PresalesAgent()

    merged_requirements, agent_reply, missing_fields, provider = agent.run(
        message=message,
        history=history,
        requirement_record=requirement_record,
    )

    # ─────────────────────────────────
    # 8️⃣ Update requirement memory
    # ─────────────────────────────────

    if merged_requirements.get("project_type"):
        requirement_record.project_type = _to_str(
            merged_requirements["project_type"]
        )

    if merged_requirements.get("project_domain"):
        requirement_record.project_domain = _to_str(
            merged_requirements["project_domain"]
        )

    if merged_requirements.get("target_users"):
        requirement_record.target_users = _to_str(
            merged_requirements["target_users"]
        )

    if merged_requirements.get("platforms"):
        requirement_record.platforms = _to_str(
            merged_requirements["platforms"]
        )

    if merged_requirements.get("main_features"):
        requirement_record.main_features = _to_str(
            merged_requirements["main_features"]
        )

    if merged_requirements.get("timeline"):
        requirement_record.timeline = _to_str(
            merged_requirements["timeline"]
        )

    if merged_requirements.get("budget"):
        requirement_record.budget = _to_str(
            merged_requirements["budget"]
        )

    if merged_requirements.get("notes"):
        requirement_record.notes = _to_str(
            merged_requirements["notes"]
        )

    if merged_requirements:
        requirement_record.raw_extraction = _to_str(merged_requirements)

    db.commit()
    db.refresh(requirement_record)

    # ─────────────────────────────────
    # 9️⃣ Detect phone number
    # ─────────────────────────────────

    phone_detected_now = False
    detected_phone = _extract_phone(message)

    if detected_phone:
        # save only if it's new or customer had no phone before
        if customer.phone != detected_phone:
            customer.phone = detected_phone
            customer.meeting_requested = True
            db.commit()
            db.refresh(customer)
            phone_detected_now = True

    # ─────────────────────────────────
    # 🔟 Compute conversation state
    # ─────────────────────────────────

    state_info = get_conversation_state(requirement_record)

    # ─────────────────────────────────
    # 1️⃣1️⃣ Lead scoring
    # ─────────────────────────────────

    lead_data = calculate_lead_score(
        requirement=requirement_record,
        history=history,
        customer_phone=customer.phone,
    )

    project.lead_score = lead_data["score"]
    project.lead_status = lead_data["status"]

    if state_info["state"] == "ready_for_summary":
        project.status = ProjectStatus.QUALIFIED
    else:
        project.status = ProjectStatus.DISCOVERY

    db.commit()
    db.refresh(project)

    # ─────────────────────────────────
    # 1️⃣1️⃣½ Fix closing reply if phone already provided
    # ─────────────────────────────────

    if phone_detected_now:
        agent_reply = (
            "تمام، استلمنا رقمك ✅\n"
            "فريقنا هيتواصل معاك قريبًا لترتيب meeting ومراجعة تفاصيل المشروع."
        )
    elif customer.meeting_requested and customer.phone:
        # لو العميل بالفعل بعت الرقم قبل كده، ما نطلبوش تاني
        lower_reply = agent_reply.lower()
        if "رقم" in agent_reply or "meeting" in lower_reply:
            agent_reply = (
                "تمام، إحنا بالفعل معانا رقمك ✅\n"
                "وفريقنا هيتواصل معاك قريبًا بخصوص المشروع."
            )

    # ─────────────────────────────────
    # 1️⃣2️⃣ Save assistant message
    # ─────────────────────────────────

    assistant_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=agent_reply,
    )

    db.add(assistant_message)
    db.commit()

    # ─────────────────────────────────
    # Return response
    # ─────────────────────────────────

    return {
        "reply": agent_reply,
        "conversation_id": conversation.id,
        "project_id": project.id,
        "provider": provider,
        "requirements": merged_requirements,
        "missing_fields": missing_fields,
        "state": state_info["state"],
        "completion_score": state_info["score"],
        "completion_total": state_info["total"],
        "field_status": state_info["fields"],
        "lead_score": lead_data["score"],
        "lead_status": lead_data["status"],
        "phone": customer.phone,
        "meeting_requested": customer.meeting_requested,
    }