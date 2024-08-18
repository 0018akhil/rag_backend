from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas.document import DocumentCreate
from ..db.models.document import Document
from ..utils.document_processor import DocumentProcessor
from ..services.s3_service import S3Service
import uuid

class DocumentService:
    def __init__(self):
        self.s3_service = S3Service()
        self.document_processor = DocumentProcessor()

    async def create_document(self, db: Session, title: str, file, current_user):
        index_name = str(uuid.uuid4())
        document = DocumentCreate(title=title)
        
        parsed_document = self.document_processor.parse_document(file)
        index_document = self.document_processor.process_and_index_documents(
            parsed_document, index_name=index_name)
        
        if not index_document:
            raise HTTPException(status_code=500, detail="Error processing document")

        return Document.create(db, **document.dict(), owner_id=current_user.id, index_name=index_name)

    def get_documents(self, db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(Document).filter(Document.owner_id == user_id).offset(skip).limit(limit).all()

    def get_specific_document(self, db: Session, document_id: int):
        return db.query(Document).filter(Document.id == document_id).first()