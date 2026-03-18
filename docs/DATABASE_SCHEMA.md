```markdown
# Database Schema

This document describes the database structure used by **AI Tawasol**.

The database stores customer conversations with the AI pre-sales agent and converts them into structured project data.

---

## Entity Relationship Diagram

```mermaid
erDiagram

CUSTOMER ||--o{ CONVERSATION : has
CUSTOMER ||--o{ PROJECT : owns

CONVERSATION ||--o{ MESSAGE : contains
CONVERSATION ||--|| PROJECT : builds
CONVERSATION ||--|| PROJECT_REQUIREMENT : extracts

CUSTOMER {
int id
string external_key
string name
string email
string phone
boolean meeting_requested
datetime created_at
datetime updated_at
}

CONVERSATION {
int id
int customer_id
int project_id
string title
enum status
datetime created_at
datetime updated_at
}

MESSAGE {
int id
int conversation_id
enum role
text content
datetime created_at
}

PROJECT {
int id
int customer_id
string name
enum status
text summary
int lead_score
string lead_status
text kano_analysis
text swot_analysis
text activity_diagram
text srs_document
string next_action
datetime created_at
datetime updated_at
}

PROJECT_REQUIREMENT {
int id
int conversation_id
string project_type
string project_domain
string target_users
string platforms
text main_features
string timeline
string budget
text notes
text raw_extraction
datetime created_at
datetime updated_at
}