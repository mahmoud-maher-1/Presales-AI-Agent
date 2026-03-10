# System Architecture

This document describes the internal architecture of **AI Tawasol**.

---

# System Flow

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