
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    mongo_uri: str
    groq_api_key: str


# Import `settings` instead of reading os.environ elsewhere, so config is validated once at startup and typed everywhere.
settings = Settings()
