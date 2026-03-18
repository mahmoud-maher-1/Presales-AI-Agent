from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -------------------------
    # Database
    # -------------------------

    DATABASE_URL: str

    # -------------------------
    # Gemini
    # -------------------------

    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # -------------------------
    # OpenRouter
    # -------------------------

    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_MODEL: str = "arcee-ai/trinity-large-preview:free"

    # -------------------------
    # Groq
    # -------------------------

    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "llama3-70b-8192"

    # -------------------------
    # Config
    # -------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()