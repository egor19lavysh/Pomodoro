from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str = "pomodoro.db"
    JWT_SECRET_KEY: str = "secret"
    JWT_ENCODE_ALGORITHM: str = "HS256"


settings = Settings(
    _env_file_encoding="utf-8",
)
