from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..core.dependencies import get_db
from ..services.auth_service import AuthService
from ..schemas.user import UserCreate, User, Token

class AuthRouter:
    def __init__(self):
        self.router = APIRouter()
        self.auth_service = AuthService()

        self.router.post("/token", response_model=Token)(self.login_for_access_token)
        self.router.post("/signup", response_model=User)(self.signup)

    async def login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        return await self.auth_service.authenticate_user(form_data, db)

    def signup(self, user: UserCreate, db: Session = Depends(get_db)):
        return self.auth_service.create_user(db, user)

auth_router = AuthRouter().router