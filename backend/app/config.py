from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    postgres_url: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def database_url(self) -> str:
        """Convert postgres:// to postgresql:// for SQLAlchemy"""
        return self.postgres_url.replace("postgres://", "postgresql://", 1)


@lru_cache()
def get_settings() -> Settings:
    return Settings()
