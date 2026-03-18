```markdown
# Agent Flow

The AI agent behaves like a **Pre-Sales Engineer**.

Its main goal is to understand the client's idea, collect project requirements, identify missing information, and guide the conversation toward a structured project definition.

---

## Agent Pipeline

```mermaid
flowchart TD

A[Client Message]
A --> B[API Route]
B --> C[Message Processor]
C --> D[Find or Create Customer]
D --> E[Find or Create Conversation]
E --> F[Save User Message]
F --> G[Load Conversation History]
G --> H[Extract Requirements]
H --> I[Update Requirement Memory]
I --> J[Detect Missing Fields]
J --> K[Select Next Question]
K --> L[Generate Arabic Response]
L --> M[Save Assistant Message]
M --> N[Return Response]