"""
Функции для взаимодействия с внешним сервисом-провайдером данных о погоде.
"""
from http import HTTPStatus
from typing import Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import settings

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о погоде.
    """

    async def get_base_url(self) -> str:
        return BASE_URL

    async def _request(self, endpoint: str) -> Optional[dict]:

        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(endpoint) as response:
                return (
                    (await response.json())
                    if response.status == HTTPStatus.OK
                    else None
                )

    async def get_weather(self, location: str) -> Optional[dict]:
        """
        Получение данных о погоде.

        :param location: Город и страна
        :return:
        """

        return await self._request(
            f"{await self.get_base_url()}?units=metric&q={location}&appid={settings.API_KEY_OPENWEATHER}"
        )
