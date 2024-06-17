"""
Функции сбора информации о странах.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, Optional, FrozenSet

import aiofiles
import aiofiles.os

from clients.country import CountryClient
from clients.currency import CurrencyClient
from clients.news import COUNTRY_SHORT_NAMES, NewsClient
from clients.weather import WeatherClient
from collectors.base import BaseCollector
from collectors.models import (
    LocationDTO,
    CountryDTO,
    CurrencyRatesDTO,
    CurrencyInfoDTO,
    NewsDTO,
    WeatherInfoDTO,
)
from settings import settings


class CountryCollector(BaseCollector):
    """
    Сбор информации о странах (географическое описание).
    """

    def __init__(self) -> None:
        self.client = CountryClient()

    @staticmethod
    async def get_file_path(**kwargs: Any) -> Path:
        return settings.MEDIA_ABSOLUTE_PATH.joinpath("country.json")

    @property
    async def cache_ttl(self) -> int:
        return settings.CACHE_TTL_COUNTRY

    async def collect(self, **kwargs: Any) -> Optional[FrozenSet[LocationDTO]]:
        if await self.cache_invalid():
            # если кэш уже невалиден, то актуализируем его
            result = await self.client.get_countries()
            if result:
                result_str = json.dumps(result)
                async with aiofiles.open(await self.get_file_path(), mode="w") as file:
                    await file.write(result_str)

        # получение данных из кэша
        async with aiofiles.open(await self.get_file_path(), mode="r") as file:
            content = await file.read()

        result = json.loads(content)
        if not result:
            return None
        locations = frozenset(
            LocationDTO(
                capital=item["capital"],
                alpha2code=item["alpha2code"],
            )
            for item in result
        )

        return locations

    @classmethod
    async def read(cls) -> Optional[list[CountryDTO]]:
        """
        Чтение данных из кэша.

        :return:
        """

        try:
            print(await cls.get_file_path())
            async with aiofiles.open(await cls.get_file_path(), mode="r") as file:
                content = await file.read()
        except FileNotFoundError:
            return None

        if not content:
            return None

        items = json.loads(content)
        result_list = []
        for item in items:
            result_list.append(
                CountryDTO(
                    capital=item["capital"],
                    alpha2code=item["alpha2code"],
                    alt_spellings=item["alt_spellings"],
                    currencies={
                        CurrencyInfoDTO(code=currency["code"])
                        for currency in item["currencies"]
                    },
                    flag=item["flag"],
                    languages=item["languages"],
                    name=item["name"],
                    population=item["population"],
                    subregion=item["subregion"],
                    timezones=item["timezones"],
                    area=item["area"],
                )
            )

        return result_list


class CurrencyRatesCollector(BaseCollector):
    """
    Сбор информации о курсах валют.
    """

    def __init__(self) -> None:
        self.client = CurrencyClient()

    @staticmethod
    async def get_file_path(**kwargs: Any) -> Path:
        return settings.MEDIA_ABSOLUTE_PATH.joinpath("currency_rates.json")

    @property
    async def cache_ttl(self) -> int:
        return settings.CACHE_TTL_CURRENCY_RATES

    async def collect(self, **kwargs: Any) -> None:
        if await self.cache_invalid():
            # если кэш уже невалиден, то актуализируем его
            result = await self.client.get_rates()
            if result:
                result_str = json.dumps(result)
                async with aiofiles.open(await self.get_file_path(), mode="w") as file:
                    await file.write(result_str)

    @classmethod
    async def read(cls) -> Optional[CurrencyRatesDTO]:
        """
        Чтение данных из кэша.

        :return:
        """

        async with aiofiles.open(await cls.get_file_path(), mode="r") as file:
            content = await file.read()

        if not content:
            return None

        result = json.loads(content)

        return CurrencyRatesDTO(
            base=result["base"],
            date=result["date"],
            rates=result["rates"],
        )


class WeatherCollector(BaseCollector):
    """
    Сбор информации о прогнозе погоды для столиц стран.
    """

    def __init__(self) -> None:
        self.client = WeatherClient()

    @staticmethod
    async def get_file_path(filename: str = "", **kwargs: Any) -> Path:
        # return f"{settings.MEDIA_PATH}/weather/{filename}.json"
        return settings.MEDIA_ABSOLUTE_PATH.joinpath("weather").joinpath(
            f"{filename}.json"
        )

    @property
    async def cache_ttl(self) -> int:
        return settings.CACHE_TTL_WEATHER

    async def collect(
        self, locations: FrozenSet[LocationDTO] = frozenset(), **kwargs: Any
    ) -> None:

        target_dir_path = f"{settings.MEDIA_ABSOLUTE_PATH}/weather"
        # если целевой директории еще не существует, то она создается
        if not await aiofiles.os.path.exists(target_dir_path):
            await aiofiles.os.mkdir(target_dir_path)

        for location in locations:
            filename = f"{location.capital}_{location.alpha2code}".lower()
            if await self.cache_invalid(filename=filename):
                # если кэш уже невалиден, то актуализируем его
                result = await self.client.get_weather(
                    f"{location.capital},{location.alpha2code}"
                )
                if result:
                    result_str = json.dumps(result)
                    async with aiofiles.open(
                        await self.get_file_path(filename), mode="w"
                    ) as file:
                        await file.write(result_str)

    @classmethod
    async def read(cls, location: LocationDTO) -> Optional[WeatherInfoDTO]:
        """
        Чтение данных из кэша.

        :param location:
        :return:
        """

        filename = f"{location.capital}_{location.alpha2code}".lower()
        async with aiofiles.open(await cls.get_file_path(filename), mode="r") as file:
            content = await file.read()

        result = json.loads(content)
        if not result:
            return None
        return WeatherInfoDTO(
            temp=result["main"]["temp"],
            pressure=result["main"]["pressure"],
            humidity=result["main"]["humidity"],
            wind_speed=result["wind"]["speed"],
            description=result["weather"][0]["description"],
            visibility=result["visibility"],
            timezone=result["timezone"],
        )


class NewsCollector(BaseCollector):
    """
    Сбор новостей для стран.
    """

    def __init__(self) -> None:
        self.client = NewsClient()

    @staticmethod
    async def get_file_path(filename: str = "", **kwargs: Any) -> Path:
        return settings.MEDIA_ABSOLUTE_PATH.joinpath("news").joinpath(
            f"{filename}.json"
        )

    @property
    async def cache_ttl(self) -> int:
        return settings.CACHE_TTL_NEWS

    async def collect(self, **kwargs: Any) -> None:

        target_dir_path = settings.MEDIA_ABSOLUTE_PATH.joinpath("news")
        # если целевой директории еще не существует, то она создается
        if not await aiofiles.os.path.exists(target_dir_path):
            await aiofiles.os.mkdir(target_dir_path)

        countries = await self._get_countries_names()
        for country_name in countries:
            short_country_name = country_name.split("_")[-1]
            if short_country_name not in COUNTRY_SHORT_NAMES:
                continue
            if await self.cache_invalid(filename=country_name):
                # если кэш уже невалиден, то актуализируем его
                result = await self.client.get_news(short_country_name)
                if result and result["totalResults"] > 0:
                    result_str = json.dumps(result)
                    async with aiofiles.open(
                        await self.get_file_path(country_name), mode="w"
                    ) as file:
                        await file.write(result_str)

    @staticmethod
    async def _get_countries_names() -> list[str]:
        """
        Получение названий стран с их короткими названиями (alpha2code).
        """
        async with aiofiles.open(
            settings.MEDIA_ABSOLUTE_PATH.joinpath("country.json"), mode="r"
        ) as file:
            content = await file.read()

        items = json.loads(content)
        return [
            f"{item['name'].replace(' ', '_')}_{item['alpha2code']}".lower()
            for item in items
        ]

    @classmethod
    async def read(cls, country_name: str) -> list[NewsDTO] | None:
        """
        Чтение данных из кэша.

        :param country_name:
        :return:
        """

        try:
            async with aiofiles.open(
                await cls.get_file_path(country_name), mode="r"
            ) as file:
                content = await file.read()
        except FileNotFoundError:
            return None

        result = json.loads(content)
        if not result:
            return None
        return [
            NewsDTO(
                author=item["author"],
                title=item["title"],
                description=item["description"],
                publishedAt=item["publishedAt"],
                content=item["content"],
                url=item["url"],
            )
            for item in result["articles"]
        ]


class Collectors:
    @staticmethod
    async def gather() -> tuple:
        return await asyncio.gather(
            CurrencyRatesCollector().collect(),
            CountryCollector().collect(),
        )

    @staticmethod
    def collect() -> None:
        loop = asyncio.get_event_loop()
        try:
            results = loop.run_until_complete(Collectors.gather())
            loop.run_until_complete(WeatherCollector().collect(results[1]))
            loop.run_until_complete(NewsCollector().collect())
            loop.run_until_complete(loop.shutdown_asyncgens())

        finally:
            loop.close()


if __name__ == "__main__":
    print(Collectors().collect())
