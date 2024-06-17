"""
Функции для взаимодействия с внешним сервисом-провайдером данных о курсах валют.
"""
from http import HTTPStatus
from typing import Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import settings


BASE_URL = "https://api.apilayer.com/fixer/latest"


class CurrencyClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о курсах валют.
    """

    async def get_base_url(self) -> str:
        return BASE_URL

    async def _request(self, endpoint: str) -> Optional[dict]:

        # формирование заголовков запроса
        headers = {"apikey": settings.API_KEY_APILAYER}

        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(endpoint, headers=headers) as response:
                return (
                    (await response.json())
                    if response.status == HTTPStatus.OK
                    else None
                )

    async def get_rates(self, base: str = "rub") -> Optional[dict]:
        """
         Получение данных о курсах валют.

        :param base: Базовая валюта
        :return:
        """

        return await self._request(f"{await self.get_base_url()}?base={base}")
