from app.agent.next_question_engine import generate_next_question
from app.agent.requirements_extractor import extract_requirements


class PresalesAgent:
    def _merge_requirements(self, requirement_record, new_requirements: dict) -> dict:
        merged_requirements = {}

        if requirement_record:
            merged_requirements = {
                "project_type": requirement_record.project_type,
                "project_domain": requirement_record.project_domain,
                "target_users": requirement_record.target_users,
                "platforms": requirement_record.platforms,
                "main_features": requirement_record.main_features,
                "timeline": requirement_record.timeline,
                "budget": requirement_record.budget,
                "notes": requirement_record.notes,
            }

        for key, value in new_requirements.items():
            if value:
                merged_requirements[key] = value

        return merged_requirements

    def _should_offer_closing(self, merged_requirements: dict, missing_fields: list[str]) -> bool:
        if not missing_fields:
            return True

        core_fields = [
            "project_type",
            "project_domain",
            "target_users",
            "platforms",
        ]

        core_ready = all(merged_requirements.get(field) for field in core_fields)

        optional_count = 0
        for field in ["main_features", "timeline", "budget"]:
            if merged_requirements.get(field):
                optional_count += 1

        return core_ready and optional_count >= 1

    def _build_closing_message(self, merged_requirements: dict) -> str:
        if not merged_requirements.get("budget"):
            return (
                "ممتاز، كده الصورة بقت واضحة بنسبة كبيرة. "
                "ممكن تقولّي كمان الميزانية المتوقعة أو الرينج المناسب ليك؟"
            )

        if not merged_requirements.get("timeline"):
            return (
                "تمام جدًا، كده عندنا تصور واضح عن المشروع. "
                "فاضل أعرف منك بس الوقت المتوقع اللي حابب المشروع يجهز فيه؟"
            )

        return (
            "ممتاز، كده الصورة بقت واضحة جدًا. "
            "لو تحب نقدر نلخص متطلبات المشروع بشكل منظم، "
            "ولو مناسب ليك تبعت رقم الموبايل علشان نرتب معاك meeting."
        )

    def run(
        self,
        message: str,
        history: str,
        requirement_record,
    ) -> tuple[dict, str, list[str], str]:

        # 1) Extract new requirements from the latest message
        new_requirements = extract_requirements(message, history)

        # 2) Merge extracted data with existing requirement record
        merged_requirements = self._merge_requirements(
            requirement_record=requirement_record,
            new_requirements=new_requirements,
        )

        # 3) Generate next question based on UPDATED requirements
        agent_reply, missing_fields, provider = generate_next_question(
            requirement=merged_requirements,
            history=history,
        )

        # 4) Closing logic
        if self._should_offer_closing(merged_requirements, missing_fields):
            agent_reply = self._build_closing_message(merged_requirements)

        return merged_requirements, agent_reply, missing_fields, provider