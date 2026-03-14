from pydantic import BaseModel


class MessageRequest(BaseModel):
    customer_key: str
    message: str


class MessageResponse(BaseModel):
    reply: str
    conversation_id: int
    provider: str
    requirements: dict
    missing_fields: list[str]
    state: str
    completion_score: int


class ProjectSummaryResponse(BaseModel):
    conversation_id: int
    summary: dict
    kano_analysis: dict | None = None
    srs_document: dict | None = None
