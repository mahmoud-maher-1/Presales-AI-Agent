# Software Requirements Specification (SRS)

## AI Tawasol — AI Pre-Sales Agent System

> **Document Version:** 1.0  
> **Date:** March 13, 2026  
> **Status:** Draft  
> **Language:** English (default) — Arabic translation available upon request  
> **Classification:** Confidential — Internal Use Only

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Architecture & Design](#3-system-architecture--design)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Data Requirements](#6-data-requirements)
7. [External Interface Requirements](#7-external-interface-requirements)
8. [System Constraints & Assumptions](#8-system-constraints--assumptions)
9. [Acceptance Criteria](#9-acceptance-criteria)
10. [Appendices](#10-appendices)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the complete functional and non-functional requirements for **AI Tawasol** (Arabic: تواصل — "communication"), an AI-powered pre-sales engineering system designed for software houses and digital agencies operating primarily in Arabic-speaking markets.

This document serves as the authoritative reference for:

- Development team implementation guidance
- QA test case derivation
- Stakeholder alignment on system capabilities
- Future enhancement planning

### 1.2 Scope

AI Tawasol automates the initial discovery phase of software project pre-sales by:

- Engaging potential clients in natural Arabic conversation
- Extracting structured project requirements from free-text messages
- Detecting missing information across 7 critical requirement categories
- Generating intelligent, context-aware follow-up questions
- Tracking conversation progress via a state machine with completion scoring
- Classifying identified features using the Kano Model
- Producing structured project summaries for handoff to human sales teams

The system is **not** a general-purpose chatbot. It is a purpose-built AI Pre-Sales Engineer focused exclusively on software project requirement discovery.

### 1.3 Intended Audience

| Audience | Purpose |
|---|---|
| Software Engineers | Implementation reference and API contracts |
| QA Engineers | Test case derivation and acceptance criteria |
| Product Owners | Feature scope validation and priority alignment |
| DevOps Engineers | Infrastructure and deployment specifications |
| Stakeholders | Business capability overview and roadmap alignment |

### 1.4 Definitions, Acronyms & Abbreviations

| Term | Definition |
|---|---|
| **SRS** | Software Requirements Specification |
| **LLM** | Large Language Model |
| **NLP** | Natural Language Processing |
| **ORM** | Object-Relational Mapping |
| **ASGI** | Asynchronous Server Gateway Interface |
| **CRUD** | Create, Read, Update, Delete |
| **REST** | Representational State Transfer |
| **Kano Model** | A product development framework that classifies features into categories based on customer satisfaction impact |
| **Pre-sales** | The process of qualifying leads and gathering requirements before producing a formal proposal |
| **Requirement Extraction** | The automated process of identifying structured project requirements from unstructured natural language text |
| **Cascading Fallback** | A pattern where multiple LLM providers are tried sequentially until one succeeds |

### 1.5 References

| Reference | Description |
|---|---|
| IEEE 830-1998 | IEEE Recommended Practice for Software Requirements Specifications |
| FastAPI Documentation | https://fastapi.tiangolo.com |
| SQLAlchemy 2.0 Documentation | https://docs.sqlalchemy.org/en/20/ |
| Google Gemini API | https://ai.google.dev/docs |
| Kano Model (Wikipedia) | https://en.wikipedia.org/wiki/Kano_model |

---

## 2. Overall Description

### 2.1 Product Perspective

AI Tawasol is a standalone backend system designed as the intelligent core of a broader pre-sales automation platform. It operates as a REST API server that can be integrated with multiple client-facing channels.

```
┌────────────────────────────────────────────────────────────────────┐
│                      External Channels                             │
│  ┌──────────┐   ┌──────────────┐   ┌───────────┐   ┌──────────┐  │
│  │  Web Chat │   │  Telegram Bot │   │ WhatsApp  │   │ Embedded │  │
│  │    (✅)    │   │    (Planned) │   │ (Planned) │   │  Widget  │  │
│  └─────┬────┘   └──────┬───────┘   └─────┬─────┘   └────┬─────┘  │
│        └────────────────┼─────────────────┼──────────────┘        │
│                         │                 │                        │
│                         ▼                 ▼                        │
│              ┌──────────────────────────────────┐                  │
│              │    AI Tawasol REST API Server     │                  │
│              │  ┌────────────────────────────┐   │                  │
│              │  │   AI Agent Pipeline (LLM)  │   │                  │
│              │  └────────────────────────────┘   │                  │
│              │  ┌────────────────────────────┐   │                  │
│              │  │   PostgreSQL Database       │   │                  │
│              │  └────────────────────────────┘   │                  │
│              └──────────────────────────────────┘                  │
└────────────────────────────────────────────────────────────────────┘
```

### 2.2 Product Features (High-Level)

| # | Feature | Priority | Status |
|---|---|---|---|
| F1 | Arabic-first conversational AI interaction | P0 — Critical | ✅ Implemented |
| F2 | LLM-based requirement extraction from free text | P0 — Critical | ✅ Implemented |
| F3 | 7-field structured requirement schema | P0 — Critical | ✅ Implemented |
| F4 | Missing field detection with priority ordering | P0 — Critical | ✅ Implemented |
| F5 | Intelligent next-question generation (non-repetitive) | P0 — Critical | ✅ Implemented |
| F6 | Full conversation memory and history tracking | P0 — Critical | ✅ Implemented |
| F7 | Multi-provider LLM with cascading fallback | P1 — High | ✅ Implemented |
| F8 | Conversation state machine with completion scoring | P1 — High | ✅ Implemented |
| F9 | Structured project summary generation | P1 — High | ✅ Implemented |
| F10 | Kano Model feature classification | P2 — Medium | ✅ Implemented |
| F11 | Minimal web-based chat UI (testing) | P2 — Medium | ✅ Implemented |
| F12 | Full SRS document auto-generation | P2 — Medium | 🔲 Planned |
| F13 | External channel integrations (Telegram, WhatsApp) | P3 — Low | 🔲 Planned |
| F14 | Admin dashboard for lead review | P3 — Low | 🔲 Planned |
| F15 | Voice/audio client interaction | P3 — Low | 🔲 Planned |

### 2.3 User Classes & Characteristics

| User Class | Description | Interface | Technical Level |
|---|---|---|---|
| **Client (End User)** | Potential customer exploring a software project idea. Communicates in Arabic or English. | Chat interface (web, Telegram, WhatsApp) | Non-technical |
| **Sales Engineer** | Internal team member reviewing conversation transcripts and extracted requirements. | API / Dashboard (planned) | Semi-technical |
| **System Administrator** | Manages deployment, configuration, and monitoring. | CLI, Docker, environment configuration | Technical |
| **Developer** | Extends, maintains, and debugs the system. | Source code, API documentation | Highly technical |

### 2.4 Operating Environment

| Component | Specification |
|---|---|
| **Runtime** | Python 3.12+ |
| **Web Framework** | FastAPI 0.135.1 (ASGI) |
| **ASGI Server** | Uvicorn 0.41.0 |
| **Database** | PostgreSQL 16 (containerized via Docker) |
| **Containerization** | Docker Compose |
| **Hosting** | Local development / Hugging Face Spaces / Cloud VM |
| **OS Compatibility** | Windows, macOS, Linux |

### 2.5 Design & Implementation Constraints

| Constraint | Description |
|---|---|
| **C1** | Primary AI responses MUST be in Egyptian Arabic dialect (عامية مصرية) |
| **C2** | The system MUST support at least one LLM provider to function |
| **C3** | All LLM interactions are synchronous (blocking calls) |
| **C4** | The system uses server-side table creation (`Base.metadata.create_all`) instead of migration-based schema management at runtime |
| **C5** | CORS is configured with permissive `allow_origins=["*"]` for development flexibility |
| **C6** | No authentication or authorization layer is implemented in the current version |
| **C7** | The system does not support concurrent conversations per customer — only one `OPEN` conversation per customer at a time |

### 2.6 Assumptions & Dependencies

| # | Assumption / Dependency |
|---|---|
| A1 | At least one LLM API key (Gemini, Groq, or OpenRouter) is available and valid |
| A2 | PostgreSQL 16 is available and reachable at the configured `DATABASE_URL` |
| A3 | Client messages are predominantly in Arabic (Egyptian dialect), with English as a secondary language |
| A4 | Internet connectivity is available for LLM API calls |
| A5 | The Docker runtime is available for running the PostgreSQL container |
| A6 | LLM providers maintain their current API contracts and response formats |

---

## 3. System Architecture & Design

### 3.1 Architectural Pattern

The system follows a **layered architecture** with clear separation of concerns:

```
┌──────────────────────────────────────────────────┐
│              Presentation Layer                    │
│   (FastAPI Routes + Static Frontend)              │
├──────────────────────────────────────────────────┤
│              Application Logic Layer               │
│   (Agent Pipeline + Message Processor)            │
├──────────────────────────────────────────────────┤
│              Service Layer                         │
│   (LLM Service + Provider Adapters)               │
├──────────────────────────────────────────────────┤
│              Data Access Layer                     │
│   (SQLAlchemy ORM + Session Management)           │
├──────────────────────────────────────────────────┤
│              Infrastructure Layer                  │
│   (PostgreSQL + Docker + Configuration)           │
└──────────────────────────────────────────────────┘
```

### 3.2 Component Overview

| Component | Module Path | Responsibility |
|---|---|---|
| **API Layer** | `app/api/` | HTTP request handling, routing, response serialization |
| **Agent Pipeline** | `app/agent/` | Core AI intelligence: requirement extraction, question generation, state management |
| **LLM Services** | `app/services/` | Provider-agnostic LLM interaction with cascading fallback |
| **Data Models** | `app/models/` | SQLAlchemy ORM entity definitions |
| **Schemas** | `app/schemas/` | Pydantic request/response validation models |
| **Configuration** | `app/core/` | Environment-based settings via pydantic-settings |
| **Database Infra** | `app/db/` | Engine, session factory, dependency injection |
| **Frontend** | `app/static/` | Minimal HTML/CSS/JS chat interface |

### 3.3 Request Processing Pipeline

Every incoming client message is processed through a **9-step sequential pipeline**:

```
    Client Message (POST /api/message)
         │
         ▼
    ┌─────────────────────────────────────────┐
    │  Step 1: Resolve Customer               │
    │  Find by external_key or create new     │
    ├─────────────────────────────────────────┤
    │  Step 2: Resolve Conversation           │
    │  Find OPEN conversation or create new   │
    ├─────────────────────────────────────────┤
    │  Step 3: Save User Message              │
    │  Persist to messages table              │
    ├─────────────────────────────────────────┤
    │  Step 4: Load Conversation History      │
    │  Retrieve all messages, format as text  │
    ├─────────────────────────────────────────┤
    │  Step 5: Resolve Requirement Record     │
    │  Find or create ProjectRequirement      │
    ├─────────────────────────────────────────┤
    │  Step 6: Run PresalesAgent              │
    │  ┌─ Phase A: Extract Requirements (LLM)│
    │  └─ Phase B: Generate Next Question(LLM)│
    ├─────────────────────────────────────────┤
    │  Step 7: Update Requirement Memory      │
    │  Merge extracted fields into DB record  │
    ├─────────────────────────────────────────┤
    │  Step 8: Calculate Conversation State   │
    │  Compute state + completion score       │
    ├─────────────────────────────────────────┤
    │  Step 9: Save Assistant Message         │
    │  Persist AI reply to messages table     │
    └─────────────────────────────────────────┘
         │
         ▼
    Response: { reply, conversation_id, provider,
                requirements, missing_fields, state,
                completion_score }
```

### 3.4 LLM Provider Cascade

The system implements a multi-provider failover strategy:

```
┌──────────┐     fail     ┌──────────┐     fail     ┌─────────────┐     fail     ┌──────────┐
│  Gemini  │ ───────────▶ │   Groq   │ ───────────▶ │ OpenRouter  │ ───────────▶ │ Fallback │
│ (Primary)│              │(Secondary)│              │ (Tertiary)  │              │  (None)  │
└──────────┘              └──────────┘              └─────────────┘              └──────────┘
```

| Provider | SDK/Client | Default Model | Timeout |
|---|---|---|---|
| **Gemini** (Primary) | `google-genai` native SDK | `gemini-2.5-flash` | SDK default |
| **Groq** (Secondary) | `httpx` REST (OpenAI-compatible) | `groq-2-latest` | 60 seconds |
| **OpenRouter** (Tertiary) | `httpx` REST (OpenAI-compatible) | `arcee-ai/trinity-large-preview:free` | 60 seconds |
| **Fallback** | None | None | N/A |

**Fallback behavior:** If all three providers fail, the system returns a hardcoded Arabic error message and `provider: "none"`.

---

## 4. Functional Requirements

### 4.1 Conversational Message Processing

#### FR-4.1.1 — Message Ingestion

| Property | Value |
|---|---|
| **ID** | FR-4.1.1 |
| **Priority** | P0 — Critical |
| **Input** | `customer_key: string`, `message: string` |
| **Trigger** | `POST /api/message` |

**Description:**  
The system SHALL accept client messages containing free-text in Arabic or English along with a customer identifier. Each message SHALL be persisted and processed through the full agent pipeline.

**Acceptance Criteria:**

1. The system SHALL accept a JSON body with `customer_key` (string) and `message` (string) fields
2. The system SHALL return HTTP 422 if either field is missing or has an invalid type
3. The system SHALL persist the user message to the `messages` table before processing
4. The system SHALL persist the AI response to the `messages` table after processing
5. The response SHALL include: `reply`, `conversation_id`, `provider`, `requirements`, `missing_fields`, `state`, `completion_score`

#### FR-4.1.2 — Customer Resolution

| Property | Value |
|---|---|
| **ID** | FR-4.1.2 |
| **Priority** | P0 — Critical |
| **Trigger** | Every incoming message |

**Description:**  
The system SHALL resolve the customer identity using the provided `customer_key`. If no customer exists with the given key, a new customer record SHALL be created automatically.

**Acceptance Criteria:**

1. Given a `customer_key` that matches an existing customer's `external_key`, the system SHALL associate the message with that customer
2. Given a `customer_key` that does NOT match any existing customer, the system SHALL create a new `Customer` record with that `external_key`
3. The system SHALL NOT create duplicate customers for the same `customer_key`

#### FR-4.1.3 — Conversation Management

| Property | Value |
|---|---|
| **ID** | FR-4.1.3 |
| **Priority** | P0 — Critical |
| **Trigger** | Every incoming message |

**Description:**  
The system SHALL maintain conversation sessions per customer. Each customer SHALL have at most one `OPEN` conversation at any time. New messages are routed to the existing open conversation or trigger creation of a new one.

**Acceptance Criteria:**

1. If the customer has an existing `OPEN` conversation, the message SHALL be added to that conversation
2. If the customer has no `OPEN` conversation, a new conversation SHALL be created with status `OPEN`
3. An `OPEN` conversation SHALL accumulate all messages until explicitly closed or archived
4. Conversation history SHALL be loaded in chronological order (ascending by `id`)

### 4.2 AI-Powered Requirement Extraction

#### FR-4.2.1 — Structured Requirement Extraction

| Property | Value |
|---|---|
| **ID** | FR-4.2.1 |
| **Priority** | P0 — Critical |
| **Trigger** | Step 6 (Phase A) of the message pipeline |

**Description:**  
The system SHALL use an LLM to extract structured project requirements from the client's free-text message. The extraction operates on the current message combined with the full conversation history.

**Requirement Schema (7 Fields):**

| Field | Type | Valid Values | Description |
|---|---|---|---|
| `project_type` | `string \| null` | `"mobile_app"`, `"web_app"` | The type of software project |
| `project_domain` | `string \| null` | `"delivery"`, `"ecommerce"`, `"booking"`, `"education"`, `"healthcare"` | The business domain |
| `target_users` | `string \| null` | Free text | Who the software is for |
| `platforms` | `string \| null` | Free text (e.g., `"Android, iOS"`) | Target deployment platforms |
| `main_features` | `string \| null` | Free text | Key features requested |
| `timeline` | `string \| null` | Free text (e.g., `"3 months"`) | Desired delivery timeline |
| `budget` | `string \| null` | Free text (e.g., `"50000 EGP"`) | Budget range or amount |

**Arabic-to-English Mapping Rules:**

| Arabic Keyword | English Value |
|---|---|
| تطبيق | `project_type: "mobile_app"` |
| موقع | `project_type: "web_app"` |
| توصيل | `project_domain: "delivery"` |
| متجر | `project_domain: "ecommerce"` |
| حجز | `project_domain: "booking"` |
| تعليم | `project_domain: "education"` |
| عيادة / طبي | `project_domain: "healthcare"` |

**Acceptance Criteria:**

1. The system SHALL send an extraction prompt to the LLM with the current message and conversation history
2. The LLM response SHALL be parsed as JSON conforming to the 7-field schema
3. Unknown fields SHALL be returned as `null`
4. If JSON parsing fails, the system SHALL return an empty dictionary `{}` (graceful degradation)
5. Extracted fields SHALL be incrementally merged into the persistent `ProjectRequirement` record (existing non-null values are NOT overwritten with null)

#### FR-4.2.2 — Missing Field Detection

| Property | Value |
|---|---|
| **ID** | FR-4.2.2 |
| **Priority** | P0 — Critical |
| **Trigger** | Step 6 (Phase B) of the message pipeline |

**Description:**  
The system SHALL detect which requirement fields are still missing (null or empty) and return them in priority order.

**Field Priority Order (highest → lowest):**

```
project_type → project_domain → platforms → target_users → main_features → timeline → budget
```

**Acceptance Criteria:**

1. A field SHALL be considered "missing" if its value is `null` or an empty/whitespace-only string
2. Missing fields SHALL be returned in the defined priority order
3. When all 7 fields are filled, the missing fields list SHALL be empty `[]`

#### FR-4.2.3 — Topic-Aware Deduplication

| Property | Value |
|---|---|
| **ID** | FR-4.2.3 |
| **Priority** | P1 — High |
| **Trigger** | During missing field detection |

**Description:**  
The system SHALL analyze conversation history to identify already-discussed topics and filter them from the missing fields list, preventing repetitive questioning.

**Topic Detection Keywords:**

| Topic | Detection Keywords (Arabic + English) |
|---|---|
| `project_type` | تطبيق, موقع, ويب, system, app, website |
| `project_domain` | توصيل, مطاعم, متجر, حجز, تعليم, عيادة, طبي |
| `platforms` | android, ios, iphone, منصة, ويب, لوحة تحكم |
| `target_users` | مستخدم, عميل, مندوب, سائق, إدارة, admin |
| `main_features` | مميزات, خصائص, دفع, تتبع, إشعارات, لوحة تحكم |
| `timeline` | مدة, ميعاد, وقت, timeline, جاهز, شهر, أسبوع |
| `budget` | ميزانية, budget, تكلفة, سعر |

**Acceptance Criteria:**

1. The system SHALL scan the full conversation history (case-insensitive) for topic keywords
2. Topics with matching keywords SHALL be excluded from the missing fields list
3. If ALL missing fields have been discussed, the filter SHALL be removed and all missing fields returned (to allow necessary re-inquiry)

### 4.3 Intelligent Question Generation

#### FR-4.3.1 — Next Question Engine

| Property | Value |
|---|---|
| **ID** | FR-4.3.1 |
| **Priority** | P0 — Critical |
| **Trigger** | Step 6 (Phase B) of the message pipeline |

**Description:**  
The system SHALL generate the single best next question to ask the client using an LLM, informed by known requirements, missing fields, asked topics, and conversation history.

**Acceptance Criteria:**

1. The generated question SHALL be in **Egyptian Arabic dialect** (عامية مصرية)
2. The system SHALL ask exactly **ONE** question per turn
3. The question SHALL NOT repeat already-discussed topics unless all remaining fields have been discussed
4. The question SHALL NOT ask about budget until project scope is reasonably clear
5. If no missing fields remain, the system SHALL return a fixed rule-based Arabic completion message without making an LLM call
6. If the LLM returns an empty response, a generic Arabic fallback question SHALL be used

**Completion Message (Rule-Based):**  
When all requirement fields are filled:
> "تمام كده، الصورة بقت واضحة دلوقتي. عايز ألخصلك متطلبات المشروع بشكل منظم؟"

**Fallback Message:**  
When LLM returns empty:
> "ممكن توضحلي أكتر عن المشروع؟"

### 4.4 Conversation State Management

#### FR-4.4.1 — State Machine

| Property | Value |
|---|---|
| **ID** | FR-4.4.1 |
| **Priority** | P1 — High |
| **Trigger** | Step 8 of the message pipeline |

**Description:**  
The system SHALL track conversation progress through a three-state state machine based on the completeness of requirement fields.

**State Definitions:**

| State | Condition | Description |
|---|---|---|
| `insufficient_information` | Fewer than 2 fields filled | Not enough data for meaningful discovery |
| `discovery_in_progress` | 2+ fields filled, but core set incomplete | Actively collecting requirements |
| `ready_for_summary` | All 4 core fields filled + at least 1 bonus field | Sufficient data for structured summary |

**Core Fields (required for `ready_for_summary`):**
1. `project_type`
2. `project_domain`
3. `target_users`
4. `platforms`

**Bonus Fields (at least 1 required for `ready_for_summary`):**
1. `main_features`
2. `timeline`
3. `budget`

**State Transition Diagram:**
```
                  ┌──────────────────────────────┐
                  │   insufficient_information    │
                  │   (filled < 2)                │
                  └──────────────┬───────────────┘
                                 │ filled >= 2
                                 ▼
                  ┌──────────────────────────────┐
                  │   discovery_in_progress       │
                  │   (filled >= 2, ¬core_ready)  │
                  └──────────────┬───────────────┘
                                 │ core_ready + bonus
                                 ▼
                  ┌──────────────────────────────┐
                  │   ready_for_summary           │
                  │   (4 core + 1 bonus)          │
                  └──────────────────────────────┘
```

#### FR-4.4.2 — Completion Scoring

| Property | Value |
|---|---|
| **ID** | FR-4.4.2 |
| **Priority** | P1 — High |

**Description:**  
The system SHALL calculate a completion score (integer 0–7) representing the number of filled requirement fields.

**Acceptance Criteria:**

1. Each of the 7 requirement fields that has a non-null, non-empty value SHALL count as 1 toward the score
2. The score SHALL be returned in every message response
3. The maximum score SHALL be 7 (all fields filled)

### 4.5 Project Summary & Analysis

#### FR-4.5.1 — Project Summary Generation

| Property | Value |
|---|---|
| **ID** | FR-4.5.1 |
| **Priority** | P1 — High |
| **Trigger** | `GET /api/conversation/{conversation_id}/summary` |

**Description:**  
The system SHALL generate a structured project summary containing all 8 fields (7 requirement fields + `notes`) from the `ProjectRequirement` record.

**Response Structure:**
```json
{
  "conversation_id": 1,
  "summary": {
    "project_type": "mobile_app",
    "project_domain": "delivery",
    "target_users": "...",
    "platforms": "...",
    "main_features": "...",
    "timeline": "...",
    "budget": "...",
    "notes": null
  },
  "kano_analysis": { ... }
}
```

**Acceptance Criteria:**

1. The system SHALL return HTTP 404 if no `ProjectRequirement` record exists for the given conversation
2. The summary SHALL include all 8 fields, including those that are `null`
3. The response SHALL include a `kano_analysis` field (may be `null` if classification fails)

#### FR-4.5.2 — Kano Model Feature Classification

| Property | Value |
|---|---|
| **ID** | FR-4.5.2 |
| **Priority** | P2 — Medium |
| **Trigger** | During summary generation |

**Description:**  
The system SHALL use an LLM to classify features identified in the conversation into Kano Model categories, providing bilingual (English/Arabic) analysis.

**Kano Categories:**

| Category | Description | Client Signal |
|---|---|---|
| `must_be` | Basic/Expected features | Necessity, urgency, non-negotiable |
| `performance` | One-dimensional features | "The better X, the better" |
| `attractive` | Delighter features | "It would be nice if", "bonus" |
| `indifferent` | Neutral features | Lack of emphasis |
| `reverse` | Unwanted features | Explicit rejection, "please don't include" |

**Output Schema:**
```json
{
  "features": [
    {
      "feature_en": "English feature name",
      "feature_ar": "Arabic feature name",
      "category": "must_be | performance | attractive | indifferent | reverse",
      "reason_en": "English classification reason",
      "reason_ar": "Arabic classification reason"
    }
  ],
  "strategic_recommendation_en": "...",
  "strategic_recommendation_ar": "..."
}
```

**Acceptance Criteria:**

1. Features SHALL be identified from the ENTIRE conversation history, not just the `main_features` field
2. Each feature SHALL be classified into exactly ONE Kano category
3. All text fields SHALL be provided in both English and Arabic
4. If LLM classification fails, the `kano_analysis` field SHALL be `null` (graceful degradation)
5. If no features can be identified, an empty `features` array SHALL be returned

### 4.6 LLM Provider Management

#### FR-4.6.1 — Multi-Provider Fallback

| Property | Value |
|---|---|
| **ID** | FR-4.6.1 |
| **Priority** | P1 — High |

**Description:**  
The system SHALL support multiple LLM providers with automatic cascading fallback. If the primary provider fails, the system SHALL automatically try the next provider in the chain.

**Acceptance Criteria:**

1. The system SHALL try providers in order: Gemini → Groq → OpenRouter
2. Each provider failure SHALL be logged with the error details
3. If all providers fail, the system SHALL return a hardcoded Arabic error message
4. The response SHALL include which provider successfully handled the request
5. Provider API keys SHALL be validated at instantiation time — missing keys trigger `ValueError`, causing fallback to the next provider

#### FR-4.6.2 — Provider Configuration

| Property | Value |
|---|---|
| **ID** | FR-4.6.2 |
| **Priority** | P1 — High |

**Description:**  
Each LLM provider SHALL be independently configurable via environment variables.

**Configuration Parameters:**

| Provider | API Key Variable | Model Variable | Default Model |
|---|---|---|---|
| Gemini | `GEMINI_API_KEY` | `GEMINI_MODEL` | `gemini-2.5-flash` |
| Groq | `GROQ_API_KEY` | `GROQ_MODEL` | `groq-2-latest` |
| OpenRouter | `OPENROUTER_API_KEY` | `OPENROUTER_MODEL` | `arcee-ai/trinity-large-preview:free` |

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

| ID | Requirement | Target |
|---|---|---|
| **NFR-5.1.1** | API response time (end-to-end, including 2 LLM calls) | < 15 seconds (95th percentile) |
| **NFR-5.1.2** | Database query latency | < 100ms per query |
| **NFR-5.1.3** | LLM provider timeout | 60 seconds per provider |
| **NFR-5.1.4** | Concurrent user support (initial) | 10–50 simultaneous users |

### 5.2 Reliability & Availability

| ID | Requirement | Description |
|---|---|---|
| **NFR-5.2.1** | LLM resilience | System SHALL remain functional via cascading fallback even if 2 of 3 LLM providers are unavailable |
| **NFR-5.2.2** | Data persistence | All messages and requirements SHALL survive application restart (PostgreSQL persistence) |
| **NFR-5.2.3** | Graceful degradation | JSON parsing failures in LLM responses SHALL NOT crash the system; empty results are returned |
| **NFR-5.2.4** | Docker auto-restart | PostgreSQL container SHALL use `restart: unless-stopped` policy |

### 5.3 Security Requirements

| ID | Requirement | Description |
|---|---|---|
| **NFR-5.3.1** | API key protection | LLM API keys SHALL be stored in `.env` file and never committed to version control |
| **NFR-5.3.2** | Database credentials | Database credentials SHALL be stored in `.env` file |
| **NFR-5.3.3** | CORS policy | CORS SHALL be restricted to specific origins in production (currently `*` for development) |
| **NFR-5.3.4** | Authentication (Planned) | API endpoints SHALL require authentication in production deployments |
| **NFR-5.3.5** | Input validation | All API inputs SHALL be validated via Pydantic schemas before processing |

### 5.4 Scalability Requirements

| ID | Requirement | Description |
|---|---|---|
| **NFR-5.4.1** | Horizontal scaling | The stateless API design SHALL support horizontal scaling behind a load balancer |
| **NFR-5.4.2** | Database scaling | PostgreSQL SHALL support connection pooling for multi-instance deployments |
| **NFR-5.4.3** | LLM provider extensibility | New LLM providers SHALL be addable by creating a new service class and updating the fallback chain |

### 5.5 Maintainability & Code Quality

| ID | Requirement | Description |
|---|---|---|
| **NFR-5.5.1** | Modular architecture | Each module SHALL have a single, well-defined responsibility |
| **NFR-5.5.2** | Type annotations | All function signatures SHALL include Python type hints |
| **NFR-5.5.3** | Configuration externalization | All environment-specific values SHALL be configurable via `.env` without code changes |
| **NFR-5.5.4** | Dependency injection | Database sessions SHALL be injected via FastAPI's `Depends()` mechanism |

### 5.6 Internationalization (i18n)

| ID | Requirement | Description |
|---|---|---|
| **NFR-5.6.1** | Primary language | AI agent responses SHALL be in Egyptian Arabic dialect by default |
| **NFR-5.6.2** | Bilingual data fields | Kano Model analysis SHALL provide both English and Arabic for all text fields |
| **NFR-5.6.3** | Arabic input processing | The system SHALL correctly process Arabic text, including right-to-left characters and Arabic numerals |
| **NFR-5.6.4** | Bilingual keyword detection | Topic deduplication SHALL recognize keywords in both Arabic and English |

---

## 6. Data Requirements

### 6.1 Entity-Relationship Model

```
┌──────────────┐       ┌─────────────────┐       ┌──────────────┐
│   CUSTOMER   │       │  CONVERSATION   │       │   MESSAGE    │
│──────────────│       │─────────────────│       │──────────────│
│ id (PK)      │──┐    │ id (PK)         │──┐    │ id (PK)      │
│ external_key │  │    │ customer_id (FK)│  │    │ convo_id (FK)│
│ name         │  ├───▶│ project_id (FK) │  ├───▶│ role (ENUM)  │
│ email        │  │    │ title           │  │    │ content      │
│ phone        │  │    │ status (ENUM)   │  │    │ created_at   │
│ created_at   │  │    │ created_at      │  │    └──────────────┘
│ updated_at   │  │    │ updated_at      │  │
└──────────────┘  │    └─────────────────┘  │
                  │            │             │
                  │            ▼             │
                  │    ┌─────────────────┐   │
                  │    │    PROJECT      │   │
                  │    │─────────────────│   │
                  ├───▶│ id (PK)         │   │
                  │    │ customer_id (FK)│   │
                  │    │ name            │   │
                  │    │ status (ENUM)   │   │
                  │    │ summary         │   │
                  │    │ created_at      │   │
                  │    │ updated_at      │   │
                  │    └─────────────────┘   │
                  │                          │
                  │    ┌─────────────────────┐│
                  │    │ PROJECT_REQUIREMENT ││
                  │    │─────────────────────││
                  │    │ id (PK)             ││
                  │    │ conversation_id (FK)│┘
                  │    │ project_type        │
                  │    │ project_domain      │
                  │    │ target_users        │
                  │    │ platforms           │
                  │    │ main_features       │
                  │    │ timeline            │
                  │    │ budget              │
                  │    │ notes               │
                  │    │ raw_extraction      │
                  │    │ created_at          │
                  │    │ updated_at          │
                  │    └─────────────────────┘
```

### 6.2 Entity Specifications

#### 6.2.1 Customer

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `Integer` | PK, auto-increment, indexed | Unique identifier |
| `external_key` | `String(255)` | Unique, nullable | External identifier (e.g., `"web_user"`) |
| `name` | `String(255)` | Nullable | Display name |
| `email` | `String(255)` | Unique, nullable | Email address |
| `phone` | `String(50)` | Unique, nullable | Phone number |
| `created_at` | `DateTime` | Default: `utcnow` | Created timestamp |
| `updated_at` | `DateTime` | Default: `utcnow`, auto-update | Modified timestamp |

#### 6.2.2 Conversation

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `Integer` | PK, auto-increment, indexed | Unique identifier |
| `customer_id` | `Integer` | FK → `customers.id`, CASCADE | Owning customer |
| `project_id` | `Integer` | FK → `projects.id`, SET NULL, nullable | Associated project |
| `title` | `String(255)` | Nullable | Conversation title |
| `status` | `Enum` | Default: `OPEN` | `OPEN` / `CLOSED` / `ARCHIVED` |
| `created_at` | `DateTime` | Default: `utcnow` | Created timestamp |
| `updated_at` | `DateTime` | Default: `utcnow`, auto-update | Modified timestamp |

#### 6.2.3 Message

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `Integer` | PK, auto-increment, indexed | Unique identifier |
| `conversation_id` | `Integer` | FK → `conversations.id`, CASCADE | Parent conversation |
| `role` | `Enum` | Required | `USER` / `ASSISTANT` / `SYSTEM` |
| `content` | `Text` | Required | Message text content |
| `created_at` | `DateTime` | Default: `utcnow` | Message timestamp |

#### 6.2.4 Project

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `Integer` | PK, auto-increment, indexed | Unique identifier |
| `customer_id` | `Integer` | FK → `customers.id`, CASCADE | Owning customer |
| `name` | `String(255)` | Required | Project name |
| `status` | `Enum` | Default: `NEW` | `NEW` / `DISCOVERY` / `QUALIFIED` / `QUOTED` / `WON` / `LOST` / `ON_HOLD` |
| `summary` | `Text` | Nullable | Free-text summary |
| `created_at` | `DateTime` | Default: `utcnow` | Created timestamp |
| `updated_at` | `DateTime` | Default: `utcnow`, auto-update | Modified timestamp |

#### 6.2.5 ProjectRequirement

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `Integer` | PK, auto-increment, indexed | Unique identifier |
| `conversation_id` | `Integer` | FK → `conversations.id`, required | Source conversation |
| `project_type` | `String` | Nullable | `"mobile_app"` or `"web_app"` |
| `project_domain` | `String` | Nullable | e.g., `"delivery"`, `"ecommerce"` |
| `target_users` | `String` | Nullable | Target user description |
| `platforms` | `String` | Nullable | Target platforms |
| `main_features` | `Text` | Nullable | Key features (may be long) |
| `timeline` | `String` | Nullable | Desired timeline |
| `budget` | `String` | Nullable | Budget range |
| `notes` | `Text` | Nullable | Additional notes |
| `raw_extraction` | `Text` | Nullable | Raw LLM output (debug) |
| `created_at` | `DateTime(tz)` | Server default: `now()` | Created timestamp |
| `updated_at` | `DateTime(tz)` | Auto-update: `now()` | Modified timestamp |

### 6.3 Relationship Summary

| Relationship | Type | Cascade |
|---|---|---|
| Customer → Conversations | One-to-Many | DELETE |
| Customer → Projects | One-to-Many | DELETE |
| Conversation → Messages | One-to-Many | DELETE |
| Conversation → Project | Many-to-One | SET NULL |
| Conversation → ProjectRequirement | One-to-One | — |

---

## 7. External Interface Requirements

### 7.1 REST API Interface

#### 7.1.1 POST /api/message

**Purpose:** Send a client message and receive AI response with metadata.

**Request:**
```json
{
  "customer_key": "web_user",
  "message": "عايز أعمل تطبيق توصيل طلبات"
}
```

**Response (200 OK):**
```json
{
  "reply": "ممتاز! تطبيق توصيل طلبات...",
  "conversation_id": 1,
  "provider": "gemini",
  "requirements": {
    "project_type": "mobile_app",
    "project_domain": "delivery",
    "target_users": null,
    "platforms": null,
    "main_features": null,
    "timeline": null,
    "budget": null
  },
  "missing_fields": ["platforms", "target_users", "main_features", "timeline", "budget"],
  "state": "discovery_in_progress",
  "completion_score": 2
}
```

**Error Responses:**

| Status | Condition |
|---|---|
| 422 | Invalid request body (missing or wrong-type fields) |

#### 7.1.2 GET /api/conversation/{conversation_id}/summary

**Purpose:** Retrieve structured project summary with Kano analysis.

**Response (200 OK):**
```json
{
  "conversation_id": 1,
  "summary": {
    "project_type": "mobile_app",
    "project_domain": "delivery",
    "target_users": "...",
    "platforms": "...",
    "main_features": "...",
    "timeline": "...",
    "budget": "...",
    "notes": null
  },
  "kano_analysis": {
    "features": [...],
    "strategic_recommendation_en": "...",
    "strategic_recommendation_ar": "..."
  }
}
```

**Error Responses:**

| Status | Condition |
|---|---|
| 404 | No requirement record found for the conversation |

#### 7.1.3 GET /

**Purpose:** Health check endpoint.

**Response (200 OK):**
```json
{
  "service": "AI Tawasol",
  "status": "running",
  "docs": "/docs",
  "chat": "/chat"
}
```

#### 7.1.4 GET /chat

**Purpose:** Serve the static chat HTML page for browser testing.

#### 7.1.5 GET /docs

**Purpose:** Auto-generated Swagger/OpenAPI interactive documentation (provided by FastAPI).

### 7.2 LLM Provider Interfaces

#### 7.2.1 Google Gemini API

| Property | Value |
|---|---|
| SDK | `google-genai` (v1.66.0) |
| Authentication | API key |
| Method | `client.models.generate_content()` |
| Error Handling | Raises `RuntimeError` on `ClientError` |

#### 7.2.2 Groq (xAI) API

| Property | Value |
|---|---|
| Endpoint | `https://api.x.ai/v1/chat/completions` |
| Protocol | REST (OpenAI-compatible) |
| Authentication | Bearer token |
| HTTP Client | `httpx` with 60s timeout |
| Response Parsing | `data["choices"][0]["message"]["content"]` |

#### 7.2.3 OpenRouter API

| Property | Value |
|---|---|
| Endpoint | `https://openrouter.ai/api/v1/chat/completions` |
| Protocol | REST (OpenAI-compatible) |
| Authentication | Bearer token |
| Extra Headers | `HTTP-Referer`, `X-Title` |
| HTTP Client | `httpx` with 60s timeout |
| Response Parsing | `data["choices"][0]["message"]["content"]` |

### 7.3 Database Interface

| Property | Value |
|---|---|
| DBMS | PostgreSQL 16 |
| Connection | `DATABASE_URL` environment variable |
| ORM | SQLAlchemy 2.0 (mapped columns) |
| Session Management | `sessionmaker` with `autoflush=False`, `autocommit=False` |
| Dependency Injection | FastAPI `Depends(get_db)` |

### 7.4 User Interface

The system includes a minimal web-based chat interface for testing:

| Component | Technology | Description |
|---|---|---|
| `chat.html` | HTML5 | Single-page chat layout with Arabic placeholder text |
| `chat.js` | Vanilla JS | Message sending via `fetch()`, DOM manipulation, summary retrieval |
| `style.css` | CSS3 | Card layout (600×80vh), blue/gray message bubbles, RTL-friendly |

---

## 8. System Constraints & Assumptions

### 8.1 Technical Constraints

| # | Constraint |
|---|---|
| TC-1 | The system operates in synchronous mode — each API request blocks until both LLM calls complete |
| TC-2 | Only one `OPEN` conversation per customer is supported |
| TC-3 | LLM prompt templates are hardcoded in `app/agent/prompts.py` and not externally configurable |
| TC-4 | The requirement schema is fixed at 7 fields — adding new fields requires code changes in multiple modules |
| TC-5 | No WebSocket support — the chat UI uses HTTP polling (send-and-wait) |
| TC-6 | No authentication or rate limiting is implemented |
| TC-7 | Database auto-creates tables on startup (no formal migration workflow at runtime) |

### 8.2 Business Constraints

| # | Constraint |
|---|---|
| BC-1 | The system is designed exclusively for software project pre-sales — it is not a general-purpose chatbot |
| BC-2 | All AI-generated responses must be in Egyptian Arabic dialect |
| BC-3 | The requirement domain mapping (Arabic → English categories) is limited to the predefined set |
| BC-4 | The system does not generate pricing or proposals — it only gathers requirements |

### 8.3 Assumptions

| # | Assumption |
|---|---|
| AS-1 | LLM providers will return valid JSON when instructed to do so in the prompt |
| AS-2 | Client messages are reasonably coherent and relate to software project requirements |
| AS-3 | The conversation will follow a progressive discovery pattern (not adversarial) |
| AS-4 | The internet connection is stable enough for multiple LLM API calls per request |

---

## 9. Acceptance Criteria

### 9.1 System-Level Acceptance Criteria

| # | Criterion | Test Method |
|---|---|---|
| AC-1 | The system starts without errors when PostgreSQL is available and at least one LLM key is configured | Startup test |
| AC-2 | A new customer is created on first message with a given `customer_key` | API test |
| AC-3 | Subsequent messages with the same `customer_key` are routed to the existing open conversation | API test |
| AC-4 | The AI responds in Egyptian Arabic dialect | Manual verification |
| AC-5 | Requirements are incrementally extracted and accumulated across multiple messages | Multi-turn API test |
| AC-6 | The completion score increases as more requirement fields are filled | Multi-turn API test |
| AC-7 | The conversation state transitions correctly: `insufficient_information` → `discovery_in_progress` → `ready_for_summary` | State validation test |
| AC-8 | If the primary LLM provider fails, the system falls back to the next provider | Provider failure simulation |
| AC-9 | If all LLM providers fail, a graceful error message in Arabic is returned | All-providers-down test |
| AC-10 | The project summary endpoint returns structured data for a valid conversation | API test |
| AC-11 | The project summary endpoint returns 404 for an invalid conversation | API test |
| AC-12 | The Kano analysis provides bilingual (EN/AR) feature classifications | Summary API test |
| AC-13 | The chat UI allows sending messages and displays responses | Browser test |

### 9.2 Requirement Extraction Acceptance Criteria

| # | Given | When | Then |
|---|---|---|---|
| RE-1 | User sends "عايز أعمل تطبيق توصيل" | Message is processed | `project_type` = `"mobile_app"`, `project_domain` = `"delivery"` |
| RE-2 | User sends "محتاج موقع لحجز المواعيد" | Message is processed | `project_type` = `"web_app"`, `project_domain` = `"booking"` |
| RE-3 | User sends "ممكن يكون على أندرويد و iOS" | Message is processed | `platforms` is populated |
| RE-4 | User has already filled `project_type` | New message mentions a different type | The existing value is NOT overwritten with null |
| RE-5 | LLM returns invalid JSON | Extraction is attempted | Empty dict `{}` is returned, no crash |

---

## 10. Appendices

### Appendix A: Technology Stack Summary

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.12+ |
| Web Framework | FastAPI | 0.135.1 |
| ASGI Server | Uvicorn | 0.41.0 |
| Database | PostgreSQL | 16 |
| ORM | SQLAlchemy | 2.0.48 |
| Migrations | Alembic | 1.18.4 (available, unused at runtime) |
| Validation | Pydantic | 2.12.5 |
| Settings | pydantic-settings | 2.13.1 |
| AI (Primary) | Google Gemini | google-genai 1.66.0 |
| AI (Fallback 1) | Groq (xAI) | via httpx 0.28.1 |
| AI (Fallback 2) | OpenRouter | via httpx 0.28.1 |
| Containerization | Docker Compose | — |
| DB Driver | psycopg2-binary | 2.9.11 |
| Frontend | HTML / CSS / JS | — |

### Appendix B: Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | ✅ Yes | — | PostgreSQL connection string |
| `GEMINI_API_KEY` | No | `""` | Google Gemini API key |
| `GEMINI_MODEL` | No | `gemini-2.5-flash` | Gemini model identifier |
| `GROQ_API_KEY` | No | `""` | Groq (xAI) API key |
| `GROQ_MODEL` | No | `groq-2-latest` | Groq model identifier |
| `OPENROUTER_API_KEY` | No | `""` | OpenRouter API key |
| `OPENROUTER_MODEL` | No | `arcee-ai/trinity-large-preview:free` | OpenRouter model identifier |

### Appendix C: File-to-Requirement Traceability Matrix

| Source File | Related Requirements |
|---|---|
| `app/api/message.py` | FR-4.1.1, FR-4.5.1 |
| `app/api/summary.py` | FR-4.5.1 |
| `app/agent/message_processor.py` | FR-4.1.1, FR-4.1.2, FR-4.1.3, FR-4.2.1, FR-4.4.1, FR-4.4.2 |
| `app/agent/presales_agent.py` | FR-4.2.1, FR-4.3.1 |
| `app/agent/requirements_extractor.py` | FR-4.2.1 |
| `app/agent/missing_fields.py` | FR-4.2.2, FR-4.2.3 |
| `app/agent/next_question_engine.py` | FR-4.3.1 |
| `app/agent/conversation_state.py` | FR-4.4.1, FR-4.4.2 |
| `app/agent/prompts.py` | FR-4.2.1, FR-4.3.1, FR-4.5.2 |
| `app/agent/summary_generator.py` | FR-4.5.1, FR-4.5.2 |
| `app/agent/kano_classifier.py` | FR-4.5.2 |
| `app/services/llm_service.py` | FR-4.6.1 |
| `app/services/gemini_service.py` | FR-4.6.1, FR-4.6.2 |
| `app/services/groq_service.py` | FR-4.6.1, FR-4.6.2 |
| `app/services/openrouter_service.py` | FR-4.6.1, FR-4.6.2 |
| `app/models/customer.py` | FR-4.1.2, Data Entity 6.2.1 |
| `app/models/conversation.py` | FR-4.1.3, Data Entity 6.2.2 |
| `app/models/message.py` | FR-4.1.1, Data Entity 6.2.3 |
| `app/models/project.py` | Data Entity 6.2.4 |
| `app/models/project_requirement.py` | FR-4.2.1, Data Entity 6.2.5 |
| `app/schemas/message.py` | FR-4.1.1, FR-4.5.1 |
| `app/core/config.py` | FR-4.6.2, NFR-5.5.3 |
| `app/db/session.py` | NFR-5.5.4 |
| `app/db/deps.py` | NFR-5.5.4 |
| `app/main.py` | NFR-5.3.3, NFR-5.5.4 |

### Appendix D: Development Roadmap

| Phase | Description | Status |
|---|---|---|
| **Phase 1** — Backend Foundation | FastAPI, PostgreSQL, Docker, ORM models, CORS, health check | ✅ Complete |
| **Phase 2** — AI Integration | Gemini, Groq, OpenRouter providers with cascading fallback | ✅ Complete |
| **Phase 3** — Pre-Sales Intelligence | Requirement extraction, missing field detection, next-question engine, state machine | ✅ Complete |
| **Phase 4** — Project Structuring | Structured requirements, summary generation, SRS auto-generation, project lifecycle | 🔶 In Progress |
| **Phase 5** — Integrations | Telegram bot, WhatsApp Business API, website chat widget, admin dashboard | 🔲 Planned |

### Appendix E: Glossary (Arabic/English)

| Arabic Term | Transliteration | English Translation |
|---|---|---|
| تواصل | Tawāṣul | Communication |
| تطبيق | Taṭbīq | Application / Mobile App |
| موقع | Mawqi' | Website |
| توصيل | Tawṣīl | Delivery |
| متجر | Matjar | Store / E-commerce |
| حجز | Ḥajz | Booking / Reservation |
| تعليم | Ta'līm | Education |
| عيادة | 'Iyāda | Clinic / Healthcare |
| مستخدم | Mustakhdim | User |
| ميزانية | Mīzāniyya | Budget |
| مميزات | Mumayyazāt | Features |
| عامية مصرية | 'Āmmiyya Maṣriyya | Egyptian Colloquial Arabic |

---

> **Document Prepared By:** AI Tawasol Development Team  
> **Last Updated:** March 13, 2026  
> **Next Review Date:** Upon Phase 4 completion
