
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
A --> B[API Route]
B --> C[Message Processor]
C --> D[Find or Create Customer]
D --> E[Find or Create Conversation]
E --> F[Save User Message]
F --> G[Load Conversation History]
G --> H[Extract Requirements]
H --> I[Update Project Requirement Memory]
I --> J[Detect Missing Fields]
J --> K[Select Next Best Question]
K --> L[Generate Natural Arabic Reply]
L --> M[Save Assistant Message]
M --> N[Return Response]

---

### What the Agent Stores

The system stores two kinds of information:

## 1. Conversation Data

customer

conversation

messages

## 2. Structured Requirement Data

project_type

project_domain

target_users

platforms

main_features

timeline

budget

notes

raw_extraction