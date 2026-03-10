def build_extraction_prompt(message: str, history: str | None = None) -> str:
    return f"""
You are an AI system that extracts software project requirements from a client message.

Return ONLY valid JSON.
Do not return markdown.
Do not explain anything.
Do not add any extra text.

Schema:
{{
  "project_type": null,
  "project_domain": null,
  "target_users": null,
  "platforms": null,
  "main_features": null,
  "timeline": null,
  "budget": null
}}

Rules:
- If the client mentions an app or تطبيق → project_type = "mobile_app"
- If the client mentions website or موقع → project_type = "web_app"
- If the project is about delivery or توصيل → project_domain = "delivery"
- If the project is about ecommerce or متجر → project_domain = "ecommerce"
- If the project is about booking or حجز → project_domain = "booking"
- If the project is about education or تعليم → project_domain = "education"
- If the project is about healthcare or عيادة or طبي → project_domain = "healthcare"
- If a field is unknown return null

Conversation history:
{history or ""}

Client message:
{message}
"""
def build_next_question_prompt(
    known: dict,
    missing: list[str],
    asked_topics: list[str],
    history: str,
) -> str:
    import json

    return f"""
You are an Arabic AI pre-sales engineer for a software house.

Your task is to ask the single best next question to understand the client's software project.

Known information:
{json.dumps(known, ensure_ascii=False, indent=2)}

Still missing information:
{json.dumps(missing, ensure_ascii=False, indent=2)}

Topics already discussed:
{json.dumps(asked_topics, ensure_ascii=False, indent=2)}

Conversation history:
{history}

Rules:
- Reply in Arabic only
- Ask only ONE question
- Do not ask a generic question
- Do not repeat a topic that was already discussed unless absolutely necessary
- Ask about budget only after scope is reasonably clear
- Choose the highest-value next question
- Focus on clarifying project scope, users, platforms, features, timeline, and budget
- Keep it concise and natural
"""