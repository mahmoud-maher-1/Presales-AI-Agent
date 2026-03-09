
---

# 2️⃣ docs/ARCHITECTURE.md

```markdown
# System Architecture

This document describes how the system works.

---

## System Flow

```mermaid
flowchart TD

A[API Route]
A --> B[Message Processor]
B --> C[Customer & Conversation Resolution]
C --> D[Save User Message]
D --> E[Load Conversation History]
E --> F[Agent Service]
F --> G[Save Assistant Message]
G --> H[Return Response]

```markdown

## Components
API Layer

Receives requests from the client.

Message Processor

Responsible for:

managing conversations

storing messages

calling the AI service

AI Service

Communicates with the AI model (Gemini).

Database

Stores:

customers

conversations

messages

projects

```
