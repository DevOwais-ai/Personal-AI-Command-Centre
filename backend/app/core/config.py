from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Personal AI Command Center"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"

    DATABASE_URL: str

    API_PREFIX: str = "/api"

    CORS_ORIGINS: str = "http://localhost:3000"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    


settings = Settings()