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
You are an Egyptian Arabic AI pre-sales engineer for a software house.

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
- Reply in Egyptian Arabic dialect only (عامية مصرية)
- Ask only ONE question
- Do not ask a generic question
- Do not repeat a topic that was already discussed unless absolutely necessary
- Ask about budget only after scope is reasonably clear
- Choose the highest-value next question
- Focus on clarifying project scope, users, platforms, features, timeline, and budget
- Keep it concise and natural
"""


def build_kano_classification_prompt(
    requirement_summary: dict,
    history: str,
) -> str:
    import json

    return f"""
You are a product strategy analyst. Your task is to classify the features and requirements
discussed in a software project conversation using the Kano Model.

## Kano Model Categories

1. **must_be** (Basic/Expected): Features the client considers essential. Their absence causes
   strong dissatisfaction, but their presence is taken for granted. Look for phrases indicating
   necessity, urgency, or non-negotiable requirements.

2. **performance** (One-Dimensional): Features where more is better — satisfaction scales
   proportionally with how well they are delivered. Look for phrases comparing quality levels
   or expressing "the better X, the better."

3. **attractive** (Delighters): Features that would pleasantly surprise the client. Their absence
   does NOT cause dissatisfaction, but their presence creates excitement. Look for phrases like
   "it would be nice if", "bonus", "if possible."

4. **indifferent**: Features mentioned in passing that the client does not seem to care strongly
   about either way. Look for lack of emphasis or enthusiasm.

5. **reverse**: Features the client explicitly does NOT want or would be unhappy to see included.
   Look for rejection, negative sentiment, or "please don't include."

## Input Data

Current extracted requirements:
{json.dumps(requirement_summary, ensure_ascii=False, indent=2)}

Full conversation history:
{history}

## Your Task

1. Read the FULL conversation history carefully.
2. Identify every distinct feature, capability, or requirement mentioned by the client.
3. Classify each feature into exactly ONE Kano category based on how the client described it
   (tone, urgency, emphasis, language used).
4. Provide a brief reason for the classification.
5. Generate a strategic recommendation summarizing what the development team should prioritize.

## Output Format

Return ONLY valid JSON. No markdown. No extra text. Follow this exact schema:

{{
  "features": [
    {{
      "feature_en": "English feature name",
      "feature_ar": "Arabic feature name",
      "category": "must_be | performance | attractive | indifferent | reverse",
      "reason_en": "English reason for classification",
      "reason_ar": "Arabic reason for classification"
    }}
  ],
  "strategic_recommendation_en": "English strategic recommendation",
  "strategic_recommendation_ar": "Arabic strategic recommendation"
}}

Rules:
- Identify features from the ENTIRE conversation, not just the main_features field
- Each feature must be classified into exactly one category
- Provide both English and Arabic for all text fields
- The strategic recommendation should advise what to build first based on Kano priorities
- Return at least the features that are clearly identifiable from the conversation
- If no features can be identified, return an empty features array
"""