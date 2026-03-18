from sqlalchemy import create_engine, text
from app.services.pdf_generator import (
    generate_summary_pdf,
    generate_swot_pdf,
    generate_kano_pdf,
    generate_activity_diagram_pdf,
    generate_history_pdf,
)

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ai_tawasol"

engine = create_engine(DATABASE_URL)

class Msg:
    def __init__(self, role, content, created_at):
        self.role = role
        self.content = content
        self.created_at = created_at

with engine.connect() as conn:
    req = conn.execute(text("""
        SELECT *
        FROM project_requirements
        WHERE conversation_id = 1
        ORDER BY id DESC
        LIMIT 1
    """)).mappings().first()

    project = conn.execute(text("""
        SELECT *
        FROM projects
        WHERE id = 1
        LIMIT 1
    """)).mappings().first()

    messages = conn.execute(text("""
        SELECT role, content, created_at
        FROM messages
        WHERE conversation_id = 1
        ORDER BY created_at
    """)).fetchall()

summary_data = {
    "project_type": req["project_type"],
    "project_domain": req["project_domain"],
    "target_users": req["target_users"],
    "platforms": req["platforms"],
    "main_features": req["main_features"],
    "timeline": req["timeline"],
    "budget": req["budget"],
    "notes": req["notes"],
}

import json

swot_data = json.loads(project["swot_analysis"]) if project["swot_analysis"] else {}
kano_data = json.loads(project["kano_analysis"]) if project["kano_analysis"] else {}

activity_data = {
    "title": project["name"] + " Activity Flow",
    "steps": [
        "Open app",
        "Login",
        "Book appointment",
        "Receive confirmation",
    ],
    "mermaid": project["activity_diagram"],
}

history_messages = [Msg(m[0], m[1], m[2]) for m in messages]

with open("summary_from_db.pdf", "wb") as f:
    f.write(generate_summary_pdf(summary_data))

with open("swot_from_db.pdf", "wb") as f:
    f.write(generate_swot_pdf(swot_data))

with open("kano_from_db.pdf", "wb") as f:
    f.write(generate_kano_pdf(kano_data))

with open("activity_from_db.pdf", "wb") as f:
    f.write(generate_activity_diagram_pdf(activity_data))

with open("history_from_db.pdf", "wb") as f:
    f.write(generate_history_pdf(history_messages, conversation_id=1, customer_name="Ahmed Ali"))

print("PDFs created successfully from database.")