from fastapi import FastAPI

from app.api.message import router as message_router
from app.db.session import Base, engine
import app.models  # noqa: F401

app = FastAPI(title="AI Tawasol API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(message_router, prefix="/api")
