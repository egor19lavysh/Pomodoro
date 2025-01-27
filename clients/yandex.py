from dataclasses import dataclass
from settings import Settings
from schema import GoogleUserData, YandexUserData
import httpx


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = self._get_user_access_token(code)
        async with self.async_client as client:
            user_info = await client.get(
                "https://login.yandex.ru/info?format=json",
                headers={"Authorization": f'OAuth {access_token}'}
            )
        return YandexUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.YANDEX_CLIENT_ID,
            "client_secret": self.settings.YANDEX_CLIENT_SECRET,
            "grant_type": "authorization_code",
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        async with self.async_client as client:
            response = await client.post("https://oauth.yandex.ru/token", data=data, headers=headers)
            access_token = response.json()["access_token"]

        return access_token
