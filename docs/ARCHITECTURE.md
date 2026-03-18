```markdown
# System Architecture

This document describes the internal architecture of **AI Tawasol**.

AI Tawasol is an **AI-powered pre-sales system** designed to collect software project requirements through conversational interaction and convert them into structured business data.

---

## Architecture Overview

The system follows a modular layered architecture built around:

- API endpoints
- database-backed conversation storage
- agent orchestration
- LLM service abstraction
- structured project generation

---

## System Flow

```mermaid
flowchart TD

A[Client Message]
A --> B[API Route]
B --> C[Message Processor]
C --> D[Resolve Customer]
D --> E[Resolve Conversation]
E --> F[Save User Message]
F --> G[Load Conversation History]
G --> H[AI Agent Service]
H --> I[Generate Response]
I --> J[Save Assistant Message]
J --> K[Return Response]