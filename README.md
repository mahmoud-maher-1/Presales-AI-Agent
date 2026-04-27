# AI Tawasol

**AI Tawasol** is an AI-powered **Presales Engineer Assistant** designed to help software companies understand client needs, analyze project opportunities, and automatically generate technical documentation.

Instead of manually conducting long discovery calls and writing technical documents, the system uses AI to guide conversations, extract requirements, and produce structured project analysis.

AI Tawasol transforms early-stage client conversations into actionable technical insights.

---

# What Problem Does It Solve

Software companies often spend significant time during the presales phase:

* Understanding vague client ideas
* Extracting structured requirements
* Writing documentation
* Evaluating project feasibility

AI Tawasol automates much of this process.

The system behaves like an **AI Presales Engineer** that:

* Asks intelligent discovery questions
* Extracts project requirements
* Analyzes the opportunity
* Generates technical documentation automatically

---

# Key Capabilities

## Intelligent Client Conversation

AI Tawasol guides the conversation with the client to clarify the project idea and collect the most crucial and necessary information for further development.

## Requirement Extraction

Automatically extracts structured project requirements including:

* Project type
* Target users
* Platforms
* Key features
* Budget
* Timeline

## Lead Scoring

Evaluates how promising a project opportunity is based on the conversation.

## Kano Feature Analysis

Classifies product features into Kano categories:

* Must-be
* Performance
* Attractive
* Indifferent
* Reverse

## SWOT Analysis

Analyzes the project from a strategic perspective including strengths, weaknesses, opportunities, and risks.

## Activity Diagram Generation

Automatically generates a **Mermaid activity diagram** that describes the main business workflow.

## SRS Document Generation

Generates a full **Software Requirements Specification (SRS)** based on the client conversation.

## PDF Report Generation

Creates downloadable project reports for internal use or client proposals.

---

# System Architecture

```mermaid
flowchart TD

Client --> ChatAPI
ChatAPI --> MessageProcessor
MessageProcessor --> RequirementExtractor
RequirementExtractor --> LeadScoring

LeadScoring --> NextQuestion
NextQuestion --> ConversationLoop

ConversationLoop --> ProjectAnalysis

ProjectAnalysis --> Kano
ProjectAnalysis --> SWOT
ProjectAnalysis --> ActivityDiagram
ProjectAnalysis --> SRS

SRS --> PDFGenerator
```

---

# Technology Stack

### Backend

FastAPI
Python

### Database

PostgreSQL
SQLAlchemy
Alembic

### AI Providers

Gemini
OpenRouter
Groq

The system automatically falls back between providers if one fails.

### Infrastructure

Docker
Docker Compose

---

# Project Structure

```
app/
 ├ agent/        # AI reasoning modules
 ├ api/          # REST API endpoints
 ├ core/         # configuration
 ├ db/           # database setup and migrations
 ├ models/       # database models
 ├ schemas/      # API schemas
 ├ services/     # external services (LLM, PDF)
 ├ static/       # simple chat interface
 └ main.py       # FastAPI application entrypoint

docs/
 ├ AGENT_FLOW.md
 ├ ARCHITECTURE.md
 ├ DATABASE_SCHEMA.md
 ├ PROJECT_STATUS.md
 ├ ROADMAP.md
 └ SRS.md
```

---

# Running the Project Locally

## 1 Start PostgreSQL

```bash
docker compose up -d
```

---

## 2 Activate virtual environment

```bash
.venv\Scripts\Activate.ps1
```

---

## 3 Run the API

```bash
uvicorn app.main:app --reload
```

---

## 4 Open the API documentation

```
http://127.0.0.1:8000/docs
```

---

## Open the Chat Interface

```
http://127.0.0.1:8000/chat
```

---

# Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_tawasol

GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

OPENROUTER_API_KEY=
OPENROUTER_MODEL=arcee-ai/trinity-large-preview:free

GROQ_API_KEY=
GROQ_MODEL=llama3-70b-8192
```

---

# Example Workflow

1. A client describes a project idea.
2. AI Tawasol asks discovery questions.
3. The system extracts structured requirements.
4. The project is analyzed using multiple frameworks.
5. The system generates documentation including:

   * Project summary
   * Kano analysis
   * SWOT analysis
   * Activity diagram
   * SRS document
6. A downloadable PDF report is generated.

---

# Future Improvements

* AI-powered proposal generation
* CRM integration
* Architecture diagram generation
* Knowledge base integration (RAG)
* Lead management dashboard

---

# License

MIT License
