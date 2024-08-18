from pydantic import BaseModel

class ChatMessage(BaseModel):
    document_id: int
    message: str

class ChatResponse(BaseModel):
    reply: str