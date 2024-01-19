from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    drop_pending_updates: bool
    admin_chat_id: int

    sqlite_db_file: Path

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def build_sqlite_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.sqlite_db_file}"
