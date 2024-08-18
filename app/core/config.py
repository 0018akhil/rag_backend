from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chat with Any Document"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PG_DATABASE_URL: str
    ALLOWED_ORIGINS: list[str] = ["http://localhost", "http://localhost:5173", "http://139.59.76.60"]
    
    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET_NAME: str

    # API Keys
    GOOGLE_API_KEY: str
    PINECONE_API_KEY: str
    UNSTRUCTURED_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()