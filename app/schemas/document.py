from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    title: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    index_name: str
    upload_date: datetime
    owner_id: int

    class Config:
        from_attributes = True