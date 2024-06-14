"""
Тестирование функций клиента для получения информации о погоде.
"""

import pytest

from clients.weather import WeatherClient
from settings import settings


@pytest.mark.asyncio
class TestClientWeather:
    """
    Тестирование клиента для получения информации о погоде.
    """

    base_url = "https://api.openweathermap.org/data/2.5/weather"

    @pytest.fixture
    def client(self):
        return WeatherClient()

    async def test_get_base_url(self, client: WeatherClient):
        assert await client.get_base_url() == self.base_url

    async def test_get_rates(self, mocker, client: WeatherClient):
        mocker.patch("clients.weather.WeatherClient._request")
        await client.get_weather("china")
        client._request.assert_called_once_with(
            f"{self.base_url}?units=metric&q=china&appid={settings.API_KEY_OPENWEATHER}"
        )
