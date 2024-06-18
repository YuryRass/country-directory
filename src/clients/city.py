"""
Функции для взаимодействия с внешним сервисом-провайдером данных о городах.
"""

from http import HTTPStatus
from typing import Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import get_settings

settings = get_settings()


class CityClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о городах.
    """

    BASE_URL = "https://api.apilayer.com/geo/city"

    async def get_base_url(self) -> str:
        return self.BASE_URL

    async def _request(self, endpoint: str) -> Optional[dict]:  # type: ignore[return]
        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(endpoint, headers=(await self.headers)) as response:
                if response.status == HTTPStatus.OK:
                    return (await response.json())[0]

    async def get_city_info(self, city_name: str) -> Optional[dict]:
        """
        Получение данных о городе.

        :param city_name: Название города
        :return:
        """

        # pylint: disable=C0209
        return await self._request(
            "{url}/name/{city}".format(
                url=(await self.get_base_url()),
                city=city_name,
            )
        )

    @property
    async def headers(self) -> dict[str, str]:
        return {"apikey": settings.API_KEY_APILAYER}
