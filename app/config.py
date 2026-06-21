import os
from pydantic_settings import BaseSettings
from pydantic import Field, AliasChoices
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = Field(default="", validation_alias=AliasChoices("DATABASE_URL", "database_url"))
    secret_key: str = Field(default="", validation_alias=AliasChoices("SECRET_KEY", "secret_key"))
    access_token_expire_minutes: int = 30
    algorithm: str = Field(default="", validation_alias=AliasChoices("ALGORITHM", "algorithm"))

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('APP_ENV', 'local')}",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

setting = Settings()
