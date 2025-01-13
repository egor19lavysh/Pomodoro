from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str = "pomodoro.db"


settings = Settings(
    _env_file_encoding="utf-8",
)
