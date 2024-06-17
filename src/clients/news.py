"""
Функции для взаимодействия с внешним сервисом-провайдером
получения последних новостей в стране.
"""
from http import HTTPStatus
from typing import Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import settings


COUNTRY_SHORT_NAMES = [
    "ae",
    "ar",
    "at",
    "au",
    "be",
    "bg",
    "br",
    "ca",
    "ch",
    "cn",
    "co",
    "cu",
    "cz",
    "de",
    "eg",
    "fr",
    "gb",
    "gr",
    "hk",
    "hu",
    "id",
    "ie",
    "il",
    "in",
    "it",
    "jp",
    "kr",
    "lt",
    "lv",
    "ma",
    "mx",
    "my",
    "ng",
    "nl",
    "no",
    "nz",
    "ph",
    "pl",
    "pt",
    "ro",
    "rs",
    "ru",
    "sa",
    "se",
    "sg",
    "si",
    "sk",
    "th",
    "tr",
    "tw",
    "ua",
    "us",
    "ve",
    "za",
]


BASE_URL = "https://newsapi.org/v2/top-headlines"


class NewsClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером
    получения последних новостей в стране.
    """

    async def get_base_url(self) -> str:
        return BASE_URL

    async def _request(self, endpoint: str, country: str = "ru") -> Optional[dict]:

        # формирование параметров запроса
        params = self._get_query_params(country)

        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(endpoint, params=params) as response:
                return (
                    (await response.json())
                    if response.status == HTTPStatus.OK
                    else None
                )

    def _get_query_params(self, country: str) -> dict[str, str]:
        return {
            "country": country,
            # business entertainment general health science sports technology
            "category": "general",
            "apiKey": settings.API_KEY_NEWS,
        }

    async def get_news(self, country: str) -> Optional[dict]:
        """
        Получение свежих новостей в стране.

        :param country: Название страны
        :return:
        """

        return await self._request(f"{await self.get_base_url()}", country)
