# AI Tawasol — Project Documentation

> **Version:** 1.0  
> **Last Updated:** March 2026  
> **Language:** Python 3.12+  
> **License:** Proprietary

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Product Vision](#2-product-vision)
3. [Core Features](#3-core-features)
4. [Technology Stack](#4-technology-stack)
5. [System Architecture](#5-system-architecture)
6. [Project Structure](#6-project-structure)
7. [Module Reference](#7-module-reference)
   - [7.1 Application Entry Point](#71-application-entry-point)
   - [7.2 API Layer](#72-api-layer)
   - [7.3 Schemas (Data Validation)](#73-schemas-data-validation)
   - [7.4 Agent Layer (AI Pipeline)](#74-agent-layer-ai-pipeline)
   - [7.5 LLM Services](#75-llm-services)
   - [7.6 Database Models (ORM)](#76-database-models-orm)
   - [7.7 Database Infrastructure](#77-database-infrastructure)
   - [7.8 Core Configuration](#78-core-configuration)
   - [7.9 Static Frontend](#79-static-frontend)
8. [Database Schema](#8-database-schema)
9. [API Reference](#9-api-reference)
10. [Agent Pipeline — Deep Dive](#10-agent-pipeline--deep-dive)
11. [LLM Provider System](#11-llm-provider-system)
12. [Conversation State Machine](#12-conversation-state-machine)
13. [Configuration & Environment Variables](#13-configuration--environment-variables)
14. [Docker & Infrastructure](#14-docker--infrastructure)
15. [Dependencies](#15-dependencies)
16. [How to Run](#16-how-to-run)
17. [Development Roadmap](#17-development-roadmap)

---

## 1. Project Overview

**AI Tawasol** (Arabic: "تواصل" — meaning "communication") is an **Arabic-first AI pre-sales agent** designed for software houses and digital agencies. It acts as an intelligent intermediary that handles the initial discovery phase of software projects by engaging potential clients in natural Arabic conversation.

The system receives client messages, understands their software project needs, asks intelligent follow-up questions about missing requirements, and progressively builds a **structured view of the project** — all before handing the qualified lead to the human sales team.

### What AI Tawasol Is

AI Tawasol is **not a chatbot**. It is an **AI Pre-Sales Engineer** that can:

- Understand client requirements from natural language (Arabic & English)
- Detect missing information across 7 critical project requirement categories
- Guide intelligent requirement discovery without repeating already-discussed topics
- Prepare structured, machine-readable project details for handoff

### Current Phase

The project is in the **Backend Foundation + AI Integration + Pre-Sales Intelligence** phase, with the following completed:

- FastAPI server with full REST API
- PostgreSQL database with Docker containerization
- Multi-provider LLM integration (Gemini, Groq, OpenRouter) with automatic fallback
- AI-powered requirement extraction from natural language
- Missing field detection and intelligent next-question generation
- Conversation state tracking with completion scoring
- Lightweight web-based chat UI for testing

---

## 2. Product Vision

AI Tawasol transforms the traditionally manual, inconsistent, and language-dependent pre-sales process into an automated, intelligent, and scalable system. The long-term vision includes:

- **Automated lead qualification** — Clients self-discover requirements through guided conversation
- **Structured deliverables** — Automatically generated Software Requirement Specifications (SRS)
- **Omnichannel presence** — Deployed across web chat, Telegram, and WhatsApp
- **Arabic-native intelligence** — Purpose-built for Arabic-speaking markets with bilingual fallback

---

## 3. Core Features

| Feature | Description | Status |
|---|---|---|
| Arabic-first AI interaction | All AI responses are generated in Arabic | ✅ Implemented |
| Requirement extraction | LLM-based extraction of project requirements from free text | ✅ Implemented |
| Structured requirement schema | 7-field standardized project requirement structure | ✅ Implemented |
| Missing field detection | Identifies which requirements are still unknown | ✅ Implemented |
| Intelligent next question | Asks the single best next question without repeating topics | ✅ Implemented |
| Conversation memory | Full message history tracking per conversation | ✅ Implemented |
| Multi-provider LLM | Gemini → Groq → OpenRouter fallback chain | ✅ Implemented |
| Conversation state machine | Tracks discovery progress with completion scoring | ✅ Implemented |
| Project summary generation | Structured summary output from extracted requirements | ✅ Implemented |
| Chat UI | Minimal web-based chat interface for testing | ✅ Implemented |
| SRS generation | Full software requirement specification output | 🔲 Planned |
| External integrations | Telegram, WhatsApp, website embed | 🔲 Planned |
| Dashboard | Admin panel for reviewing conversations | 🔲 Planned |
| Audio support | Voice-based client interaction | 🔲 Planned |

---

## 4. Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Language** | Python | 3.12+ | Core programming language |
| **Web Framework** | FastAPI | 0.135.1 | High-performance async REST API |
| **ASGI Server** | Uvicorn | 0.41.0 | ASGI application server |
| **Database** | PostgreSQL | 16 | Relational data storage |
| **ORM** | SQLAlchemy | 2.0.48 | Database abstraction layer |
| **Migrations** | Alembic | 1.18.4 | Database schema migrations |
| **Validation** | Pydantic | 2.12.5 | Request/response data validation |
| **Settings** | pydantic-settings | 2.13.1 | Environment-based configuration |
| **AI (Primary)** | Google Gemini | google-genai 1.66.0 | Primary LLM provider |
| **AI (Fallback 1)** | Groq (xAI) | via httpx | Secondary LLM provider |
| **AI (Fallback 2)** | OpenRouter | via httpx | Tertiary LLM provider |
| **HTTP Client** | httpx | 0.28.1 | Making HTTP requests to LLM APIs |
| **Containerization** | Docker Compose | — | PostgreSQL container management |
| **DB Driver** | psycopg2-binary | 2.9.11 | PostgreSQL adapter for Python |
| **Frontend** | HTML / CSS / JS | — | Minimal testing chat interface |

---

## 5. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser / API)                       │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       FastAPI Application                           │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────────┐ │
│  │  /api/message│  │ /api/summary │  │     /chat (Static UI)      │ │
│  └──────┬──────┘  └──────┬───────┘  └────────────────────────────┘ │
│         │                │                                          │
│         ▼                ▼                                          │
│  ┌─────────────────────────────────┐                                │
│  │       Message Processor         │                                │
│  │  ┌───────────┐ ┌─────────────┐  │                                │
│  │  │ Resolve   │ │  Resolve    │  │                                │
│  │  │ Customer  │ │ Conversation│  │                                │
│  │  └───────────┘ └─────────────┘  │                                │
│  │  ┌───────────────────────────┐  │                                │
│  │  │    PresalesAgent.run()    │  │                                │
│  │  │  ┌─────────────────────┐  │  │                                │
│  │  │  │ Requirements        │  │  │                                │
│  │  │  │ Extractor (LLM)     │  │  │                                │
│  │  │  └─────────────────────┘  │  │                                │
│  │  │  ┌─────────────────────┐  │  │                                │
│  │  │  │ Next Question       │  │  │                                │
│  │  │  │ Engine (LLM)        │  │  │                                │
│  │  │  └─────────────────────┘  │  │                                │
│  │  └───────────────────────────┘  │                                │
│  │  ┌───────────────────────────┐  │                                │
│  │  │  Conversation State Calc  │  │                                │
│  │  └───────────────────────────┘  │                                │
│  └─────────────────────────────────┘                                │
│                 │                                                    │
│                 ▼                                                    │
│  ┌─────────────────────────────────┐                                │
│  │        LLM Service Layer        │                                │
│  │  Gemini → Groq → OpenRouter     │                                │
│  │     (cascading fallback)        │                                │
│  └─────────────────────────────────┘                                │
│                 │                                                    │
│                 ▼                                                    │
│  ┌─────────────────────────────────┐                                │
│  │  SQLAlchemy ORM + PostgreSQL    │                                │
│  │  ┌──────────┐ ┌──────────────┐  │                                │
│  │  │ Customer │ │ Conversation │  │                                │
│  │  ├──────────┤ ├──────────────┤  │                                │
│  │  │ Message  │ │   Project    │  │                                │
│  │  ├──────────┤ └──────────────┘  │                                │
│  │  │ Project  │                   │                                │
│  │  │Requirement│                  │                                │
│  │  └──────────┘                   │                                │
│  └─────────────────────────────────┘                                │
└─────────────────────────────────────────────────────────────────────┘
```

### Request Flow (Sequence)

```
Client Message
     │
     ▼
API Route (/api/message)
     │
     ▼
Message Processor
     ├── 1. Find or create Customer
     ├── 2. Find or create open Conversation
     ├── 3. Save user Message to database
     ├── 4. Load full conversation history
     ├── 5. Find or create ProjectRequirement record
     ├── 6. Run PresalesAgent
     │       ├── a. Extract requirements (LLM call #1)
     │       ├── b. Detect missing fields
     │       └── c. Generate next question (LLM call #2)
     ├── 7. Update requirement memory in database
     ├── 8. Calculate conversation state & completion score
     └── 9. Save assistant Message to database
     │
     ▼
Return Response (reply, requirements, missing_fields, state, score)
```

---

## 6. Project Structure

```
ai-tawasol/
│
├── app/                              # Main application package
│   ├── main.py                       # FastAPI app initialization, CORS, routing, health check
│   │
│   ├── api/                          # HTTP API route handlers
│   │   ├── message.py                # POST /api/message + GET /api/conversation/{id}/summary
│   │   └── summary.py                # GET /api/conversation/{id}/summary (alternate)
│   │
│   ├── agent/                        # AI agent pipeline (core intelligence)
│   │   ├── presales_agent.py         # PresalesAgent orchestrator class
│   │   ├── message_processor.py      # Main message processing pipeline (9-step flow)
│   │   ├── requirements_extractor.py # LLM-based requirement extraction from text
│   │   ├── missing_fields.py         # Missing field detection + topic deduplication
│   │   ├── next_question_engine.py   # Intelligent next-question generation via LLM
│   │   ├── conversation_state.py     # Conversation state machine + completion scoring
│   │   ├── prompts.py                # LLM prompt templates (extraction + question gen)
│   │   └── summary_generator.py      # Project summary output builder
│   │
│   ├── services/                     # External service integrations
│   │   ├── llm_service.py            # Multi-provider LLM orchestrator (fallback chain)
│   │   ├── gemini_service.py         # Google Gemini LLM adapter
│   │   ├── groq_service.py           # xAI Groq LLM adapter
│   │   └── openrouter_service.py     # OpenRouter LLM adapter
│   │
│   ├── models/                       # SQLAlchemy ORM models
│   │   ├── __init__.py               # Model exports
│   │   ├── customer.py               # Customer entity
│   │   ├── conversation.py           # Conversation entity (with status enum)
│   │   ├── message.py                # Message entity (with role enum)
│   │   ├── project.py                # Project entity (with status lifecycle)
│   │   └── project_requirement.py    # Project requirement memory (7 fields)
│   │
│   ├── schemas/                      # Pydantic request/response schemas
│   │   └── message.py                # MessageRequest, MessageResponse, ProjectSummaryResponse
│   │
│   ├── core/                         # Application configuration
│   │   └── config.py                 # Settings class via pydantic-settings
│   │
│   ├── db/                           # Database infrastructure
│   │   ├── session.py                # SQLAlchemy engine, Base, SessionLocal
│   │   └── deps.py                   # FastAPI dependency injection for DB sessions
│   │
│   └── static/                       # Static frontend files
│       ├── chat.html                 # Chat UI HTML page
│       ├── chat.js                   # Chat client-side logic
│       └── style.css                 # Chat UI styling
│
├── docs/                             # Project documentation
│   ├── ARCHITECTURE.md               # System architecture diagram
│   ├── AGENT_FLOW.md                 # Agent pipeline flow diagram
│   ├── DATABASE_SCHEMA.md            # ER diagram of database entities
│   ├── PROJECT_STATUS.md             # Current development status
│   ├── ROADMAP.md                    # 5-phase product roadmap
│   └── images/                       # Diagram images
│
├── .env                              # Environment variables (secrets, API keys)
├── .gitignore                        # Git ignore rules
├── docker-compose.yml                # Docker Compose for PostgreSQL
├── requirements.txt                  # Python dependency lock file (56 packages)
├── README.md                         # Quick-start project README
└── PROJECT_DOCUMENTATION.md          # This file
```

---

## 7. Module Reference

### 7.1 Application Entry Point

#### `app/main.py`

The application entry point that initializes the FastAPI application instance and configures all middleware, routing, and static file serving.

**Responsibilities:**
- Creates the `FastAPI` app with title, description, and version metadata
- Configures **CORS middleware** with permissive settings (`allow_origins=["*"]`) for browser-based clients
- Registers two API routers under the `/api` prefix: `message_router` and `summary_router`
- Mounts static files from `app/static` at the `/static` URL path
- Serves the chat UI at `GET /chat` via `FileResponse`
- Provides a health check endpoint at `GET /` returning service status and useful links

**Key Endpoints Registered:**
| Method | Path | Handler |
|---|---|---|
| `GET` | `/` | `root()` — Health check |
| `GET` | `/chat` | `chat_page()` — Serves chat UI |
| `POST` | `/api/message` | Message router |
| `GET` | `/api/conversation/{id}/summary` | Summary router |

---

### 7.2 API Layer

#### `app/api/message.py`

The primary API router handling the main conversation endpoint and project summary retrieval.

**Endpoints:**

| Method | Path | Function | Description |
|---|---|---|---|
| `POST` | `/api/message` | `send_message()` | Accepts a client message and returns AI response with metadata |
| `GET` | `/api/conversation/{conversation_id}/summary` | `get_project_summary()` | Returns structured project summary for a given conversation |

**`POST /api/message`**
- Accepts a `MessageRequest` body (`customer_key: str`, `message: str`)
- Delegates to `process_message()` in the message processor
- Returns a `MessageResponse` containing the AI reply, conversation ID, provider used, extracted requirements, missing fields, conversation state, and completion score

**`GET /api/conversation/{conversation_id}/summary`**
- Looks up the `ProjectRequirement` record for the given conversation
- Raises `404` if no requirement record exists
- Returns a `ProjectSummaryResponse` with the structured summary

#### `app/api/summary.py`

An alternate summary endpoint providing a simplified summary lookup.

| Method | Path | Function | Description |
|---|---|---|---|
| `GET` | `/api/conversation/{conversation_id}/summary` | `get_conversation_summary()` | Returns raw requirement fields as a summary |

> **Note:** Both `message.py` and `summary.py` register a route at `/api/conversation/{conversation_id}/summary`. The router registered last in `main.py` (`summary_router`) would take precedence for GET requests at this path.

---

### 7.3 Schemas (Data Validation)

#### `app/schemas/message.py`

Pydantic models for API request/response validation and serialization.

**`MessageRequest`**
```python
class MessageRequest(BaseModel):
    customer_key: str     # External identifier for the customer
    message: str          # The client's message text
```

**`MessageResponse`**
```python
class MessageResponse(BaseModel):
    reply: str            # The AI-generated response text
    conversation_id: int  # Database ID of the conversation
    provider: str         # LLM provider used ("gemini", "Groq", "openrouter", "rule-based", "none")
    requirements: dict    # Extracted requirements from this message
    missing_fields: list[str]  # Fields still unknown
    state: str            # Conversation state ("insufficient_information", "discovery_in_progress", "ready_for_summary")
    completion_score: int # Number of requirement fields filled (0–7)
```

**`ProjectSummaryResponse`**
```python
class ProjectSummaryResponse(BaseModel):
    conversation_id: int
    summary: dict         # Structured project requirement summary
```

---

### 7.4 Agent Layer (AI Pipeline)

The agent layer is the core intelligence of AI Tawasol. It orchestrates the entire flow from receiving a client message to generating an intelligent Arabic response.

#### `app/agent/message_processor.py`

**Function:** `process_message(db, customer_key, message) → dict`

The central orchestrator that executes the **9-step message processing pipeline**:

| Step | Action | Description |
|---|---|---|
| 1 | Resolve Customer | Finds existing customer by `external_key` or creates a new one |
| 2 | Resolve Conversation | Finds an existing `OPEN` conversation for the customer or creates one |
| 3 | Save User Message | Persists the client's message to the `messages` table |
| 4 | Load History | Retrieves all messages in the conversation, formatted as `"ROLE: content"` |
| 5 | Resolve Requirement | Finds or creates a `ProjectRequirement` record linked to the conversation |
| 6 | Run Agent | Invokes `PresalesAgent.run()` which runs LLM extraction and question generation |
| 7 | Update Requirements | Merges newly extracted fields into the persistent requirement record |
| 8 | Calculate State | Computes the conversation state and completion score |
| 9 | Save AI Message | Persists the AI's response to the `messages` table |

**Returns:**
```python
{
    "reply": str,              # AI response text
    "conversation_id": int,    # Conversation database ID
    "provider": str,           # Which LLM provider was used
    "requirements": dict,      # Extracted requirements from this turn
    "missing_fields": list,    # Remaining unknown fields
    "state": str,              # Conversation state label
    "completion_score": int,   # Fields filled (0–7)
}
```

#### `app/agent/presales_agent.py`

**Class:** `PresalesAgent`  
**Method:** `run(message, history, requirement_record) → tuple[dict, str, list[str], str]`

A lightweight orchestrator that coordinates two LLM-powered sub-tasks:

1. **Requirement Extraction** — Calls `extract_requirements()` with the current message and conversation history
2. **Next Question Generation** — Calls `generate_next_question()` with the current requirement record and history

Returns a tuple of `(requirements_dict, agent_reply, missing_fields_list, provider_name)`.

#### `app/agent/requirements_extractor.py`

**Function:** `extract_requirements(message, history) → dict`

Extracts structured project requirements from the client's free-text message using an LLM call.

**Process:**
1. Builds an extraction prompt using `build_extraction_prompt()`
2. Sends the prompt to the LLM service
3. Parses the LLM's JSON response into a Python dictionary
4. Returns an empty dict `{}` if JSON parsing fails (graceful degradation)

**Output Schema:**
```json
{
    "project_type": "mobile_app" | "web_app" | null,
    "project_domain": "delivery" | "ecommerce" | "booking" | "education" | "healthcare" | null,
    "target_users": string | null,
    "platforms": string | null,
    "main_features": string | null,
    "timeline": string | null,
    "budget": string | null
}
```

#### `app/agent/missing_fields.py`

Handles detection of missing requirement fields and prevents repetitive questioning.

**Functions:**

| Function | Signature | Description |
|---|---|---|
| `is_missing(value)` | `→ bool` | Returns `True` if value is `None` or empty string |
| `detect_missing_fields(requirement)` | `→ list[str]` | Returns all unfilled fields in priority order |
| `build_known_requirements(requirement)` | `→ dict` | Extracts all current field values from the requirement record |
| `extract_asked_topics(history)` | `→ list[str]` | Scans conversation history for Arabic/English keywords to identify already-discussed topics |
| `detect_missing_without_repetition(requirement, history)` | `→ tuple[list, list]` | Returns filtered missing fields (excluding already-asked topics) and the list of asked topics |

**Field Priority Order:**
```
project_type → project_domain → platforms → target_users → main_features → timeline → budget
```

**Topic Detection Keywords (Arabic + English):**

| Topic | Keywords |
|---|---|
| `project_type` | تطبيق, موقع, ويب, system, app, website |
| `project_domain` | توصيل, مطاعم, متجر, حجز, تعليم, عيادة, طبي |
| `platforms` | android, ios, iphone, منصة, ويب, لوحة تحكم |
| `target_users` | مستخدم, عميل, مندوب, سائق, إدارة, admin |
| `main_features` | مميزات, خصائص, دفع, تتبع, إشعارات, لوحة تحكم |
| `timeline` | مدة, ميعاد, وقت, timeline, جاهز, شهر, أسبوع |
| `budget` | ميزانية, budget, تكلفة, سعر |

#### `app/agent/next_question_engine.py`

**Function:** `generate_next_question(requirement, history) → tuple[str, list[str], str]`

Generates the single best next question to ask the client.

**Logic:**
1. Calls `detect_missing_without_repetition()` to get filtered missing fields
2. If **no missing fields** remain → returns a fixed Arabic completion message:  
   *"ممتاز، الصورة أصبحت أوضح الآن. هل تريد أن ألخص لك متطلبات المشروع الحالية بشكل منظم؟"*  
   with provider `"rule-based"`
3. If missing fields exist → builds a prompt with known info, missing fields, asked topics, and history, then calls the LLM
4. Falls back to a generic Arabic question if the LLM returns empty text:  
   *"هل يمكنك توضيح المزيد عن المشروع؟"*

**Returns:** `(reply_text, missing_fields_list, provider_name)`

#### `app/agent/prompts.py`

Contains two prompt-building functions that construct the LLM prompts.

**`build_extraction_prompt(message, history)`**

Constructs a prompt that instructs the LLM to:
- Extract project requirements from the client message
- Return **ONLY valid JSON** (no markdown, no extra text)
- Follow specific domain-mapping rules (Arabic → English categories)
- Return `null` for unknown fields

Supports Arabic keyword mapping:
- تطبيق → `mobile_app`
- موقع → `web_app`
- توصيل → `delivery`
- متجر → `ecommerce`
- حجز → `booking`
- تعليم → `education`
- عيادة/طبي → `healthcare`

**`build_next_question_prompt(known, missing, asked_topics, history)`**

Constructs a prompt that instructs the LLM to:
- Act as an **Arabic AI pre-sales engineer**
- Ask only **ONE question** (the highest-value next question)
- Reply in **Arabic only**
- Avoid repeating already-discussed topics
- Ask about budget only after scope is reasonably clear
- Focus on: scope, users, platforms, features, timeline, budget

#### `app/agent/conversation_state.py`

Manages conversation progress tracking and state determination.

**Functions:**

**`calculate_completion_score(requirement)`**
- Checks 7 requirement fields for non-empty values
- Returns `{score: int, total: 7, fields: {field: bool, ...}}`

**`get_conversation_state(requirement)`**
- Determines the conversation state based on filled fields:

| State | Condition |
|---|---|
| `ready_for_summary` | All 4 core fields filled (`project_type`, `project_domain`, `target_users`, `platforms`) + at least 1 of (`main_features`, `timeline`, `budget`) |
| `discovery_in_progress` | At least 2 fields are filled |
| `insufficient_information` | Fewer than 2 fields are filled |

#### `app/agent/summary_generator.py`

**Function:** `generate_project_summary(requirement) → dict`

Converts a `ProjectRequirement` ORM object into a plain dictionary containing all 8 fields (the 7 requirement fields + `notes`). Used for the summary API endpoint.

---

### 7.5 LLM Services

The LLM service layer implements a **cascading fallback pattern** across three providers: Gemini (primary), Groq (secondary), and OpenRouter (tertiary).

#### `app/services/llm_service.py`

**Function:** `generate_ai_response(prompt) → dict`

The central LLM dispatcher that tries each provider in sequence:

```
Gemini → Groq → OpenRouter → Fallback (hardcoded Arabic error message)
```

**Fallback Logic:**
1. Attempts **Gemini** — if it succeeds, returns `{"provider": "gemini", "text": response}`
2. If Gemini fails (any exception), logs the error and attempts **Groq**
3. If Groq fails, logs the error and attempts **OpenRouter**
4. If all three fail, returns a hardcoded Arabic message:  
   *"عذرًا، خدمة الذكاء الاصطناعي غير متاحة حاليًا. حاول مرة أخرى بعد قليل."*  
   with `"provider": "none"`

#### `app/services/gemini_service.py`

**Class:** `GeminiService`

Uses the official `google-genai` SDK (v1.66.0).

| Aspect | Detail |
|---|---|
| SDK | `google.genai.Client` |
| Authentication | API key via `settings.GEMINI_API_KEY` |
| Default Model | `gemini-2.5-flash` |
| Method | `client.models.generate_content()` |
| Error Handling | Raises `RuntimeError` on `ClientError` |
| Fallback Text | `"عذرًا، لم أتمكن من توليد رد الآن."` if response is empty |

#### `app/services/groq_service.py`

**Class:** `GroqService`

Calls the xAI Groq API using `httpx` for HTTP requests.

| Aspect | Detail |
|---|---|
| API Endpoint | `https://api.x.ai/v1/chat/completions` |
| Authentication | Bearer token via `settings.GROQ_API_KEY` |
| Default Model | `Groq-2-latest` |
| HTTP Client | `httpx.post()` with 60s timeout |
| Response Parsing | `data["choices"][0]["message"]["content"]` |
| Logging | Prints status code and response body to console |

#### `app/services/openrouter_service.py`

**Class:** `OpenRouterService`

Calls the OpenRouter API using `httpx` for HTTP requests.

| Aspect | Detail |
|---|---|
| API Endpoint | `https://openrouter.ai/api/v1/chat/completions` |
| Authentication | Bearer token via `settings.OPENROUTER_API_KEY` |
| Default Model | `arcee-ai/trinity-large-preview:free` |
| Extra Headers | `HTTP-Referer`, `X-Title` (required by OpenRouter) |
| HTTP Client | `httpx.post()` with 60s timeout |
| Response Parsing | `data["choices"][0]["message"]["content"]` |
| Logging | Prints status code and response body to console |

---

### 7.6 Database Models (ORM)

All models use SQLAlchemy 2.0 Mapped Column declarations and inherit from a shared `Base` declarative base.

#### `app/models/customer.py` — `Customer`

Represents a client/potential customer interacting with the system.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `Integer` | PK, indexed | Auto-incrementing primary key |
| `external_key` | `String(255)` | Unique, nullable | External identifier (e.g., `"web_user"`) |
| `name` | `String(255)` | Nullable | Customer display name |
| `email` | `String(255)` | Unique, nullable | Customer email address |
| `phone` | `String(50)` | Unique, nullable | Customer phone number |
| `created_at` | `DateTime` | Default: `utcnow` | Record creation timestamp |
| `updated_at` | `DateTime` | Default: `utcnow`, auto-update | Last modification timestamp |

**Relationships:** `conversations` (one-to-many), `projects` (one-to-many)

#### `app/models/conversation.py` — `Conversation`

Represents a chat session between a customer and the AI agent.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `Integer` | PK, indexed | Auto-incrementing primary key |
| `customer_id` | `Integer` | FK → `customers.id`, CASCADE | Owning customer |
| `project_id` | `Integer` | FK → `projects.id`, SET NULL, nullable | Associated project |
| `title` | `String(255)` | Nullable | Conversation title |
| `status` | `Enum(ConversationStatus)` | Default: `OPEN` | Current conversation state |
| `created_at` | `DateTime` | Default: `utcnow` | Record creation timestamp |
| `updated_at` | `DateTime` | Default: `utcnow`, auto-update | Last modification timestamp |

**Status Enum:** `OPEN`, `CLOSED`, `ARCHIVED`  
**Relationships:** `customer` (many-to-one), `project` (many-to-one), `messages` (one-to-many)

#### `app/models/message.py` — `Message`

Represents a single message within a conversation.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `Integer` | PK, indexed | Auto-incrementing primary key |
| `conversation_id` | `Integer` | FK → `conversations.id`, CASCADE | Parent conversation |
| `role` | `Enum(MessageRole)` | Required | Who sent the message |
| `content` | `Text` | Required | Message text content |
| `created_at` | `DateTime` | Default: `utcnow` | Message timestamp |

**Role Enum:** `USER`, `ASSISTANT`, `SYSTEM`  
**Relationships:** `conversation` (many-to-one)

#### `app/models/project.py` — `Project`

Represents a qualified software project derived from conversations.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `Integer` | PK, indexed | Auto-incrementing primary key |
| `customer_id` | `Integer` | FK → `customers.id`, CASCADE | Owning customer |
| `name` | `String(255)` | Required | Project name |
| `status` | `Enum(ProjectStatus)` | Default: `NEW` | Project lifecycle stage |
| `summary` | `Text` | Nullable | Free-text project summary |
| `created_at` | `DateTime` | Default: `utcnow` | Record creation timestamp |
| `updated_at` | `DateTime` | Default: `utcnow`, auto-update | Last modification timestamp |

**Status Enum:** `NEW`, `DISCOVERY`, `QUALIFIED`, `QUOTED`, `WON`, `LOST`, `ON_HOLD`  
**Relationships:** `customer` (many-to-one), `conversations` (one-to-many)

#### `app/models/project_requirement.py` — `ProjectRequirement`

Stores the structured, incrementally-built project requirements extracted during conversation.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `Integer` | PK, indexed | Auto-incrementing primary key |
| `conversation_id` | `Integer` | FK → `conversations.id`, required | Source conversation |
| `project_type` | `String` | Nullable | e.g., `"mobile_app"`, `"web_app"` |
| `project_domain` | `String` | Nullable | e.g., `"delivery"`, `"ecommerce"`, `"healthcare"` |
| `target_users` | `String` | Nullable | Who the software is for |
| `platforms` | `String` | Nullable | Target platforms (iOS, Android, Web, etc.) |
| `main_features` | `Text` | Nullable | Key features requested |
| `timeline` | `String` | Nullable | Desired delivery timeline |
| `budget` | `String` | Nullable | Budget range or amount |
| `notes` | `Text` | Nullable | Additional free-text notes |
| `raw_extraction` | `Text` | Nullable | Raw LLM extraction output (for debugging) |
| `created_at` | `DateTime(tz)` | Server default: `now()` | Record creation timestamp |
| `updated_at` | `DateTime(tz)` | Auto-update: `now()` | Last modification timestamp |

**Relationships:** `conversation` (many-to-one)

---

### 7.7 Database Infrastructure

#### `app/db/session.py`

Configures the SQLAlchemy database engine and session factory.

- **`Base`** — The `DeclarativeBase` class that all ORM models inherit from
- **`engine`** — Created via `create_engine()` using the `DATABASE_URL` from settings, with SQL echo enabled (`echo=True`)
- **`SessionLocal`** — A `sessionmaker` bound to the engine with `autoflush=False` and `autocommit=False` for explicit transaction control

#### `app/db/deps.py`

Provides **FastAPI dependency injection** for database sessions.

**`get_db()`** — A generator function that:
1. Creates a new `SessionLocal` instance
2. Yields it for the request lifecycle
3. Closes it in the `finally` block to prevent connection leaks

Usage in routes: `db: Session = Depends(get_db)`

---

### 7.8 Core Configuration

#### `app/core/config.py`

Uses `pydantic-settings` for environment-based configuration management.

**`Settings` class** — Loads from `.env` file with `extra="ignore"`:

| Setting | Type | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | `str` | Required | PostgreSQL connection string |
| `GEMINI_API_KEY` | `str` | `""` | Google Gemini API key |
| `GEMINI_MODEL` | `str` | `"gemini-2.5-flash"` | Gemini model name |
| `OPENROUTER_API_KEY` | `str` | `""` | OpenRouter API key |
| `OPENROUTER_MODEL` | `str` | `"arcee-ai/trinity-large-preview:free"` | OpenRouter model name |
| `GROQ_API_KEY` | `str` | `""` | xAI Groq API key |
| `GROQ_MODEL` | `str` | `"Groq-2-latest"` | Groq model name |

**Singleton:** `settings = Settings()` — Instantiated at module import time.

---

### 7.9 Static Frontend

A minimal browser-based chat interface for testing and demonstration.

#### `app/static/chat.html`

A single-page HTML document with:
- Chat container with scrollable message area
- Text input with Arabic placeholder: *"اكتب رسالتك..."*
- Send button for submitting messages
- "Generate Project Summary" button

#### `app/static/chat.js`

Client-side JavaScript that handles:

- **`sendMessage()`** — POSTs to `/api/message` with `customer_key: "web_user"` and the input text, then displays both user and AI messages
- **`addMessage(text, type)`** — Creates DOM elements for messages with CSS classes `"user"` or `"ai"`, auto-scrolls to the latest message
- **`getSummary()`** — Fetches `/api/conversation/{id}/summary` and displays the JSON result in the chat
- Tracks `conversationId` across messages for summary retrieval

#### `app/static/style.css`

Clean, modern chat UI styling:
- Centered card layout (600px wide, 80vh tall) with rounded corners and box shadow
- Blue header bar (`#4a6cf7`) with white text
- User messages: blue bubbles aligned right with rounded corners
- AI messages: gray bubbles aligned left with rounded corners
- Styled input area with rounded text field and blue send button
- Hover effects on buttons

---

## 8. Database Schema

### Entity Relationship Diagram

```
┌──────────────┐       ┌─────────────────┐       ┌──────────────┐
│   CUSTOMER   │       │  CONVERSATION   │       │   MESSAGE    │
│──────────────│       │─────────────────│       │──────────────│
│ id (PK)      │──┐    │ id (PK)         │──┐    │ id (PK)      │
│ external_key │  │    │ customer_id (FK)│  │    │ convo_id (FK)│
│ name         │  ├───>│ project_id (FK) │  ├───>│ role (ENUM)  │
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
                  ├───>│ id (PK)         │   │
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

### Relationships

| Relationship | Type | Cascade |
|---|---|---|
| Customer → Conversations | One-to-Many | DELETE |
| Customer → Projects | One-to-Many | DELETE |
| Conversation → Messages | One-to-Many | DELETE |
| Conversation → Project | Many-to-One | SET NULL |
| Conversation → ProjectRequirement | One-to-One | — |

---

## 9. API Reference

### `POST /api/message`

Send a client message and receive an AI response.

**Request Body:**
```json
{
    "customer_key": "web_user",
    "message": "عايز أعمل تطبيق توصيل طلبات"
}
```

**Response Body (200 OK):**
```json
{
    "reply": "ممتاز! تطبيق توصيل طلبات. هل التطبيق ده هيكون متاح على أندرويد بس ولا iOS كمان؟",
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

### `GET /api/conversation/{conversation_id}/summary`

Retrieve the structured project requirements for a conversation.

**Response Body (200 OK):**
```json
{
    "conversation_id": 1,
    "summary": {
        "project_type": "mobile_app",
        "project_domain": "delivery",
        "target_users": "مستخدمين ومندوبين توصيل",
        "platforms": "Android, iOS",
        "main_features": "متابعة الطلبات، دفع إلكتروني، إشعارات",
        "timeline": "3 شهور",
        "budget": "50000 جنيه",
        "notes": null
    }
}
```

### `GET /`

Health check endpoint.

**Response Body (200 OK):**
```json
{
    "service": "AI Tawasol",
    "status": "running",
    "docs": "/docs",
    "chat": "/chat"
}
```

### `GET /chat`

Serves the static chat HTML page for browser testing.

### `GET /docs`

Auto-generated Swagger/OpenAPI interactive documentation (provided by FastAPI).

---

## 10. Agent Pipeline — Deep Dive

The agent pipeline executes **two LLM calls per incoming message**, making each interaction a dual-phase process:

### Phase 1: Requirement Extraction

```
User Message + History → Extraction Prompt → LLM → JSON Parsing → Requirements Dict
```

The extraction prompt instructs the LLM to act as a structured data extractor, returning only valid JSON with 7 fields. It includes language-specific rules for mapping Arabic terms to standardized categories (e.g., "تطبيق" → "mobile_app").

### Phase 2: Next Question Generation

```
Known Requirements + Missing Fields + Asked Topics + History → Question Prompt → LLM → Arabic Response
```

The question generation prompt instructs the LLM to act as an Arabic pre-sales engineer, selecting the single highest-value next question to ask. The system prevents topic repetition by:

1. Scanning the conversation history for Arabic and English keywords related to each requirement field
2. Filtering out already-discussed topics from the missing fields list
3. If all missing fields have been discussed at least once, the filter is removed (forcing re-inquiry when necessary)

### Fallback Behavior

If no missing fields remain (all 7 requirements filled), the system returns a rule-based Arabic response asking the client if they'd like a structured summary — **no LLM call is made**.

---

## 11. LLM Provider System

### Provider Cascade

The system implements a **cascading fallback** pattern where providers are tried sequentially until one succeeds:

```
┌──────────┐     fail     ┌──────────┐     fail     ┌─────────────┐     fail     ┌──────────┐
│  Gemini  │ ──────────── │   Groq   │ ──────────── │ OpenRouter  │ ──────────── │ Fallback │
│ (Primary)│              │(Secondary)│              │ (Tertiary)  │              │  (None)  │
└──────────┘              └──────────┘              └─────────────┘              └──────────┘
```

### Provider Comparison

| Provider | SDK | API Style | Default Model | Timeout |
|---|---|---|---|---|
| **Gemini** | `google-genai` | Native SDK | `gemini-2.5-flash` | SDK default |
| **Groq** | `httpx` | REST (OpenAI-compatible) | `Groq-2-latest` | 60s |
| **OpenRouter** | `httpx` | REST (OpenAI-compatible) | `arcee-ai/trinity-large-preview:free` | 60s |

### Provider Initialization

Each provider validates its API key on instantiation (`__init__`). If the API key is missing or empty, the constructor raises `ValueError`, which is caught by the fallback chain in `llm_service.py` and triggers the next provider.

---

## 12. Conversation State Machine

The system tracks conversation progress through three states based on the **completion of requirement fields**.

### State Diagram

```
                    ┌────────────────────────────┐
                    │   insufficient_information  │
                    │   (score < 2)               │
                    └─────────────┬──────────────┘
                                  │ score >= 2
                                  ▼
                    ┌────────────────────────────┐
                    │  discovery_in_progress      │
                    │  (2 ≤ score, not core-ready)│
                    └─────────────┬──────────────┘
                                  │ core_ready + bonus
                                  ▼
                    ┌────────────────────────────┐
                    │    ready_for_summary        │
                    │  (core 4 filled + 1 bonus)  │
                    └────────────────────────────┘
```

### State Definitions

| State | Condition | Meaning |
|---|---|---|
| `insufficient_information` | Fewer than 2 requirement fields filled | Not enough data to start meaningful discovery |
| `discovery_in_progress` | 2+ fields filled, but core set incomplete | Actively collecting requirements |
| `ready_for_summary` | All 4 core fields filled + at least 1 of (features/timeline/budget) | Enough data to produce a structured project summary |

### Core Fields (required for `ready_for_summary`)

1. `project_type`
2. `project_domain`
3. `target_users`
4. `platforms`

### Completion Score

An integer from 0 to 7 representing how many of the requirement fields have been filled.

---

## 13. Configuration & Environment Variables

### `.env` File

```env
# Database
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ai_tawasol

# Google Gemini (Primary LLM)
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash

# OpenRouter (Tertiary LLM)
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=openrouter/free

# Groq / xAI (Secondary LLM)
GROQ_API_KEY=your-Groq-api-key
GROQ_MODEL=openai/gpt-oss-120b
```

### Configuration Loading

Settings are loaded via `pydantic-settings` at application startup:
1. Reads from the `.env` file in the project root
2. Environment variables override `.env` values
3. `extra="ignore"` silently discards unknown environment variables
4. `DATABASE_URL` is the only **required** setting (no default)
5. All LLM-related settings default to empty strings or model names

---

## 14. Docker & Infrastructure

### `docker-compose.yml`

Provides a containerized PostgreSQL 16 instance:

```yaml
services:
  postgres:
    image: postgres:16
    container_name: ai_tawasol_postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: ai_tawasol
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Key Details:**
- Uses official `postgres:16` image
- Container named `ai_tawasol_postgres`
- Restarts automatically unless manually stopped
- Exposes port `5432` on the host
- Data persisted in a named Docker volume `postgres_data`
- Default credentials: `postgres:postgres`, database: `ai_tawasol`

---

## 15. Dependencies

The project has **56 Python packages** specified in `requirements.txt`. Key dependencies grouped by purpose:

### Web Framework
| Package | Version | Purpose |
|---|---|---|
| `fastapi` | 0.135.1 | Web framework |
| `uvicorn` | 0.41.0 | ASGI server |
| `starlette` | 0.52.1 | FastAPI's underlying ASGI toolkit |
| `pydantic` | 2.12.5 | Data validation |
| `pydantic-settings` | 2.13.1 | Settings management |

### Database
| Package | Version | Purpose |
|---|---|---|
| `SQLAlchemy` | 2.0.48 | ORM |
| `alembic` | 1.18.4 | Database migrations |
| `psycopg2-binary` | 2.9.11 | PostgreSQL adapter |
| `psycopg` | 3.3.3 | Modern PostgreSQL adapter |
| `greenlet` | 3.3.2 | SQLAlchemy async support |

### AI / LLM
| Package | Version | Purpose |
|---|---|---|
| `google-genai` | 1.66.0 | Gemini API SDK |
| `google-ai-generativelanguage` | 0.6.15 | Gemini protobuf definitions |
| `google-api-core` | 2.30.0 | Google API base library |
| `google-auth` | 2.49.0 | Google authentication |
| `httpx` | 0.28.1 | HTTP client for Groq/OpenRouter APIs |

### Utilities
| Package | Version | Purpose |
|---|---|---|
| `python-dotenv` | 1.2.2 | .env file loading |
| `websockets` | 16.0 | WebSocket support |

---

## 16. How to Run

### Prerequisites

- Python 3.12+
- Docker Desktop (for PostgreSQL)
- At least one LLM API key (Gemini recommended)

### Step-by-Step

**1. Clone the repository:**
```bash
git clone <repository-url>
cd ai-tawasol
```

**2. Create and activate a virtual environment:**
```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables:**
```bash
# Copy the .env template and fill in your API keys
# At minimum, set GEMINI_API_KEY for the primary LLM provider
```

**5. Start PostgreSQL via Docker:**
```bash
docker compose up -d
```

**6. Run the API server:**
```bash
uvicorn app.main:app --reload
```

**7. Access the application:**

| URL | Description |
|---|---|
| `http://127.0.0.1:8000` | Health check |
| `http://127.0.0.1:8000/docs` | Swagger API documentation |
| `http://127.0.0.1:8000/chat` | Chat testing UI |

---

## 17. Development Roadmap

### Phase 1 — Backend Foundation ✅

Core backend infrastructure.

- [x] FastAPI application setup
- [x] PostgreSQL with Docker
- [x] SQLAlchemy ORM models
- [x] Message endpoint (`POST /api/message`)
- [x] Customer, Conversation, Message persistence
- [x] CORS middleware
- [x] Health check endpoint

### Phase 2 — AI Integration ✅

Connecting AI model providers.

- [x] Gemini API integration (google-genai SDK)
- [x] Groq API integration (xAI REST API)
- [x] OpenRouter API integration
- [x] Multi-provider cascading fallback
- [x] Dynamic AI responses in Arabic

### Phase 3 — Pre-Sales Intelligence ✅

Requirement discovery system.

- [x] Requirements extraction via LLM
- [x] Structured 7-field requirement schema
- [x] Missing field detection with priority ordering
- [x] Topic-aware deduplication (prevents repetitive questions)
- [x] Intelligent next-question engine
- [x] Conversation state machine with completion scoring

### Phase 4 — Project Structuring 🔲

Transform conversation into structured project data.

- [x] Store structured requirements per conversation
- [x] Generate project summary endpoint
- [ ] Generate full Software Requirement Specification (SRS)
- [ ] Project lifecycle management (discovery → qualified → quoted)

### Phase 5 — Integrations 🔲

External communication channels.

- [ ] Website chat widget (embeddable)
- [ ] Telegram bot integration
- [ ] WhatsApp Business API integration
- [ ] Admin dashboard for reviewing conversations and leads

---

> **AI Tawasol** — Bridging the gap between Arabic-speaking clients and software development teams through intelligent, automated pre-sales discovery.
