"""
Тестирование функций клиента для получения свежих новостей в стране.
"""

import pytest

from clients.news import NewsClient


@pytest.mark.asyncio
class TestClientCurrency:
    """
    Тестирование клиента для получения информации о погоде.
    """

    base_url = "https://newsapi.org/v2/top-headlines"

    @pytest.fixture
    def client(self):
        return NewsClient()

    async def test_get_base_url(self, client: NewsClient):
        assert await client.get_base_url() == self.base_url

    async def test_get_news(self, mocker, client: NewsClient):
        mocker.patch("clients.news.NewsClient._request")
        await client.get_news("ch")
        client._request.assert_called_once_with(self.base_url, "ch")
