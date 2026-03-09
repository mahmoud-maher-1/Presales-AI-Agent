from pydantic import BaseModel


class MessageRequest(BaseModel):
    customer_key: str
    message: str


class MessageResponse(BaseModel):
    reply: str
    conversation_id: int
