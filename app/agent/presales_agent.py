from app.agent.conversation_state import get_conversation_state
from app.agent.requirements_extractor import extract_requirements
from app.agent.next_question_engine import generate_next_question


class PresalesAgent:
    def run(
        self,
        message: str,
        history: str,
        requirement_record,
    ) -> tuple[dict, str, list[str], str, dict]:
        requirements = extract_requirements(message, history)

        agent_reply, missing_fields, provider = generate_next_question(
            requirement=requirement_record,
            history=history,
        )

        state_info = get_conversation_state(requirement_record)

        return requirements, agent_reply, missing_fields, provider, state_info
