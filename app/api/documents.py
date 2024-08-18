from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..core.dependencies import get_current_user, get_db
from ..services.document_service import DocumentService
from ..schemas.document import Document, DocumentCreate
from ..db.models.user import User

class DocumentRouter:
    def __init__(self):
        self.router = APIRouter()
        self.document_service = DocumentService()

        self.router.post("/documents/", response_model=Document)(self.create_document)
        self.router.get("/documents/", response_model=list[Document])(self.read_documents)

    async def create_document(
        self,
        title: str = Form(...),
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        return await self.document_service.create_document(db, title, file, current_user)

    def read_documents(
        self,
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        return self.document_service.get_documents(db, current_user.id, skip, limit)

documents_router = DocumentRouter().router