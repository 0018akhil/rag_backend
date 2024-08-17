from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_documents(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Document).filter(models.Document.owner_id == user_id).offset(skip).limit(limit).all()

def get_specific_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def create_document(db: Session, document: schemas.DocumentCreate, user_id: int, s3_object_key: str):
    db_document = models.Document(**document.dict(), owner_id=user_id, s3_object_key=s3_object_key)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document