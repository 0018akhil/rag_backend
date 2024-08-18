from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import auth_router
from .api.documents import documents_router
from .api.chat import chat_router
from .core.config import settings
import os
from dotenv import load_dotenv

class Application:
    def __init__(self):
        self.app = FastAPI(title=settings.PROJECT_NAME)
        self.configure_cors()
        self.include_routers()

    def configure_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def include_routers(self):
        self.app.include_router(auth_router)
        self.app.include_router(documents_router)
        self.app.include_router(chat_router)

    def get_app(self):
        return self.app

app = Application().get_app()

@app.get("/")
async def root():
    return {"message": "Welcome to chat with any document!"}