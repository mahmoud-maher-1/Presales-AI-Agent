from app.agent.next_question_engine import generate_next_question
from app.agent.requirements_extractor import extract_requirements


class PresalesAgent:
    def run(
        self,
        message: str,
        history: str,
        requirement_record,
    ) -> tuple[dict, str, list[str], str]:
        requirements = extract_requirements(message, history)

        agent_reply, missing_fields, provider = generate_next_question(
            requirement=requirement_record,
            history=history,
        )

        return requirements, agent_reply, missing_fields, provider