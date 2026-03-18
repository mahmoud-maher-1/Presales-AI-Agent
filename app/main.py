import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.message import router as message_router
from app.api.summary import router as summary_router
from app.api.pdf import router as pdf_router
from app.db.migrate import run_migrations


# -------------------------
# Logging
# -------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("ai_tawasol")


# -------------------------
# FastAPI App
# -------------------------

app = FastAPI(
    title="AI Tawasol",
    description="AI Presales Agent API",
    version="1.0",
)


# -------------------------
# Startup
# -------------------------

@app.on_event("startup")
def on_startup():
    try:
        logger.info("Starting AI Tawasol service...")
        logger.info("Running database migrations...")

        run_migrations()

        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")


# -------------------------
# Middleware
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Routers
# -------------------------

app.include_router(message_router, prefix="/api", tags=["Chat"])
app.include_router(summary_router, prefix="/api", tags=["Analysis"])
app.include_router(pdf_router, prefix="/api", tags=["Documents"])


# -------------------------
# Static files
# -------------------------

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# -------------------------
# Pages
# -------------------------

@app.get("/chat")
def chat_page():
    return FileResponse("app/static/chat.html")


# -------------------------
# Root endpoint
# -------------------------

@app.get("/")
def root():
    return {
        "service": "AI Tawasol",
        "status": "running",
        "docs": "/docs",
        "chat": "/chat",
    }


# -------------------------
# Health check (Docker)
# -------------------------

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Tawasol",
        "version": "1.0"
    }