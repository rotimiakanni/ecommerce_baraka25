from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI E-commerce"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # DB
    DATABASE_URL: str
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""

    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str = ""
    SECRET_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
