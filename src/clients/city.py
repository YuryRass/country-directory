"""
Функции для взаимодействия с внешним сервисом-провайдером данных о городах.
"""
from http import HTTPStatus
from typing import Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import settings


class CityClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о городах.
    """

    async def get_base_url(self) -> str:
        return "https://api.apilayer.com/geo/city"

    async def _request(self, endpoint: str) -> Optional[dict]:

        # формирование заголовков запроса
        headers = {"apikey": settings.API_KEY_APILAYER}

        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == HTTPStatus.OK:
                    return (await response.json())[0]

                return None

    async def get_city_info(self, city_name: str) -> Optional[dict]:
        """
        Получение данных о городе.

        :param city_name: Название города
        :return:
        """

        return await self._request(f"{await self.get_base_url()}/name/{city_name}")
