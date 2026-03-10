# Database Schema

This document describes the core database structure of **AI Tawasol**.

---

# Entities Overview

```mermaid
erDiagram

    CUSTOMER ||--o{ CONVERSATION : has
    CONVERSATION ||--o{ MESSAGE : contains
    CONVERSATION ||--|| PROJECT : builds

    CUSTOMER {
        int id
        string name
        string email
        string company
        datetime created_at
    }

    CONVERSATION {
        int id
        int customer_id
        string status
        text summary
        datetime created_at
    }

    MESSAGE {
        int id
        int conversation_id
        string role
        text content
        datetime created_at
    }

    PROJECT {
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
    }