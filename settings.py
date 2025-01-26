from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str = "pomodoro.db"
    JWT_SECRET_KEY: str = "secret"
    JWT_ENCODE_ALGORITHM: str = "HS256"
    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_REDIRECT_URI: str = ''
    GOOGLE_CLIENT_SECRET: str = ''
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'
    YANDEX_CLIENT_ID: str = ''
    YANDEX_REDIRECT_URI: str = ''
    YANDEX_CLIENT_SECRET: str = ''

    @property
    def google_redirect_url(self) -> str:
        return f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline'

    @property
    def yandex_redirect_url(self) -> str:
        return f'https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri={self.YANDEX_REDIRECT_URI}'


settings = Settings(
    _env_file_encoding="utf-8",
)
