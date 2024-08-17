from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, documents, chat

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Welcome to chat with any document!"}