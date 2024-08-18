from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..core.security import create_access_token, verify_password
from ..db.models.user import User
from ..schemas.user import UserCreate, Token
from ..core.security import get_password_hash

class AuthService:
    def __init__(self):
        pass

    async def authenticate_user(self, form_data, db: Session):
        user = self.get_user_by_email(db, email=form_data.username)
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.email})
        return Token(access_token=access_token, token_type="bearer")

    def create_user(self, db: Session, user: UserCreate):
        db_user = self.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        user.password = get_password_hash(user.password)
        return User.create(db, **user.dict())

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()