"""
Тестирование функций сбора информации о странах.
"""
from pathlib import Path
import pytest

from collectors.collector import CountryCollector
from collectors.models import LocationDTO
from settings import get_settings

settings = get_settings()


@pytest.mark.asyncio
class TestCollectorCountry:
    """
    Тестирование коллектора для получения информации о странах.
    """

    get_countries_call_result = [
        dict(
            capital="Mariehamn",
            alpha2code="AX",
            alt_spellings=["AX", "Aaland", "Aland", "Ahvenanmaa"],
            area=1580.0,
            currencies=[
                dict(
                    code="EUR",
                )
            ],
            flag="http://assets.promptapi.com/flags/AX.svg",
            languages=[dict(name="Swedish", native_name="svenska")],
            name="\u00c5land Islands",
            population=28875,
            subregion="Northern Europe",
            timezones=[
                "UTC+02:00",
            ],
        )
    ]

    @pytest.fixture
    def collector(self):
        return CountryCollector()

    @pytest.fixture
    def file_path_for_test(self) -> Path:
        return settings.MEDIA_ABSOLUTE_PATH.joinpath("country.json")

    async def test_get_file_path(
        self, collector: CountryCollector, file_path_for_test: Path
    ):
        assert await collector.get_file_path() == file_path_for_test

    async def test_get_cache_ttl(self, collector: CountryCollector):
        """ToDo по аналогии."""

    async def test_collect_no_cache(
        self, mocker, collector: CountryCollector, file_path_for_test: Path
    ):
        mocker.patch("clients.country.CountryClient.get_countries")
        collector.client.get_countries.return_value = self.get_countries_call_result
        mocker.patch("collectors.collector.CountryCollector.cache_invalid")
        collector.cache_invalid.return_value = True
        mocker.patch("collectors.collector.CountryCollector.get_file_path")
        collector.get_file_path.return_value = file_path_for_test

        call_result = await collector.collect()
        collector.client.get_countries.assert_called_once_with()

        assert call_result == frozenset(
            {LocationDTO(capital="Mariehamn", alpha2code="AX")}
        )

    async def test_collect_from_cache(self, mocker, collector):
        """ToDO Если в кеше есть данные."""

    async def test_collect_no_cache_but_client_returns_none(self, mocker, collector):
        """ToDO Если в кеше данные невалидны, но клиент не вернул результат.

        Fixme Сейчас приложение такой кейс не разруливает. Можете написать обработку =)
        """

    async def test_read_if_file_is_absent(self, collector):
        """ToDO Если файла нет / пустой."""

    async def test_read_if_file_is_corrupted(self, collector):
        """ToDO Если файл содержит данные не в нужном формате."""

    async def test_read_ok(self, collector):
        """ToDO OK кейс."""
