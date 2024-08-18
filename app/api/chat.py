from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dependencies import get_current_user, get_db
from ..services.chat_service import ChatService
from ..schemas.chat import ChatMessage
from ..db.models.user import User

class ChatRouter:
    def __init__(self):
        self.router = APIRouter()
        self.chat_service = ChatService()

        self.router.post("/chat", response_model=dict)(self.chat_with_document)

    async def chat_with_document(
        self,
        chat_message: ChatMessage,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        return await self.chat_service.process_chat(db, chat_message, current_user)

chat_router = ChatRouter().router