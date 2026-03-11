from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.message import router as message_router
from app.api.summary import router as summary_router

app = FastAPI(
    title="AI Tawasol",
    description="AI Presales Agent API",
    version="1.0"
)

# -------------------------
# CORS (important for browser)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# API Routers
# -------------------------
app.include_router(message_router, prefix="/api")
app.include_router(summary_router, prefix="/api")

# -------------------------
# Static Files (frontend)
# -------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# -------------------------
# Chat UI
# -------------------------
@app.get("/chat")
def chat_page():
    return FileResponse("app/static/chat.html")


# -------------------------
# Health Check
# -------------------------
@app.get("/")
def root():
    return {
        "service": "AI Tawasol",
        "status": "running",
        "docs": "/docs",
        "chat": "/chat"
    }