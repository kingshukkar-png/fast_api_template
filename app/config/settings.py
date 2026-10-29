from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PORT: int = 8000
    TITLE: str = "FastAPI To-Do App"
    DESCRIPTION: str = "A simple To-Do application built with FastAPI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    MONGODB_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "todo-app"
    JWT_SECRET_KEY: str = "your_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()