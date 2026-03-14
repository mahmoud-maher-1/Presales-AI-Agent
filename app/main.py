from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.message import router as message_router
from app.api.summary import router as summary_router
from app.api.pdf import router as pdf_router

from app.db.session import engine
from app.models import Base

app = FastAPI(
    title="AI Tawasol",
    description="AI Presales Agent API",
    version="1.0"
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_router, prefix="/api")
app.include_router(summary_router, prefix="/api")
app.include_router(pdf_router, prefix="/api")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/chat")
def chat_page():
    return FileResponse("app/static/chat.html")


@app.get("/")
def root():
    return {
        "service": "AI Tawasol",
        "status": "running",
        "docs": "/docs",
        "chat": "/chat"
    }