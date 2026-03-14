from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENV: str = "dev"
    FRONTEND_ORIGIN: str = "http://localhost:3000"

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    UPLOAD_DIR: str = "./app/uploads"
    MAX_UPLOAD_MB: int = 15

settings = Settings()
