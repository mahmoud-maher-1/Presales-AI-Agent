
---

# 3️⃣ docs/AGENT_FLOW.md

```markdown
# Agent Architecture

The AI agent behaves like a pre-sales engineer.

Its goal is to understand the client's idea and collect project requirements.

---

## Agent Pipeline

```mermaid
flowchart TD

A[Client Message]

A --> B[Message Understanding]

B --> C[Requirement Extraction]

C --> D[Update Project Memory]

D --> E[Detect Missing Information]

E --> F[Select Next Question]

F --> G[Generate Natural Arabic Reply]

G --> H[Return Response]

```markdown
## Agent Steps 

Message Understanding

Interpret the client message.

Requirement Extraction

Extract structured information such as:

project_type

project_goal

platforms

features

timeline

budget

Project Memory

Save extracted information in conversation memory.

Missing Information Detection

Detect which fields are missing.

Next Question Selection

Choose the most important missing field.

Reply Generation

Generate a natural Arabic response.

```