"""
Функции для взаимодействия с внешним сервисом-провайдером данных о странах.
"""
from http import HTTPStatus
from typing import Any, Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import settings


class CountryClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о странах.
    """

    async def get_base_url(self) -> str:
        return "https://api.apilayer.com/geo/country"

    async def _request(self, *args: Any) -> Optional[dict]:

        # формирование заголовков запроса
        headers = {"apikey": settings.API_KEY_APILAYER}

        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(args[0], headers=headers) as response:
                if response.status == HTTPStatus.OK:
                    return await response.json()

                return None

    async def get_countries(self, bloc: str = "eu") -> Optional[dict]:
        """
        Получение данных о странах.

        :param bloc: Регион
        :return:
        """

        return await self._request(f"{await self.get_base_url()}/regional_bloc/{bloc}")
