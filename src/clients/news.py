"""
Функции для взаимодействия с внешним сервисом-провайдером
получения последних новостей в стране.
"""
from http import HTTPStatus
from typing import Any, Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import settings

COUNTRY_SHORT_NAMES = [
    "ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch",
    "cn", "co", "cu", "cz", "de", "eg", "fr", "gb","gr", "hk",
    "hu", "id", "ie", "il", "in", "it", "jp", "kr", "lt", "lv",
    "ma", "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt",
    "ro", "rs", "ru", "sa", "se", "sg", "si", "sk", "th", "tr",
    "tw", "ua", "us", "ve", "za",
]


class NewsClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером
    получения последних новостей в стране.
    """

    async def get_base_url(self) -> str:
        return "https://newsapi.org/v2/top-headlines"

    async def _request(self, *args: Any) -> Optional[dict]:

        # формирование параметров запроса
        params = {
            "country": args[1],
            "category": "general",  # business entertainment general health science sports technology
            "apiKey": settings.API_KEY_NEWS,
        }

        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(args[0], params=params) as response:
                if response.status == HTTPStatus.OK:
                    return await response.json()

                return None

    async def get_news(self, country: str) -> Optional[dict]:
        """
        Получение свежих новостей в стране.

        :param country: Название страны
        :return:
        """

        return await self._request(f"{await self.get_base_url()}", country)
