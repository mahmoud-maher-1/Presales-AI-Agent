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