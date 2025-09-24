"""
Configuration settings for the application.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings.
    """
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()
