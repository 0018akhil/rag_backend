# app/db/models/user.py
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from ..base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    documents = relationship("Document", back_populates="owner")

    @classmethod
    def create(cls, db, **kwargs):
        obj = cls(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj