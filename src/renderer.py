"""
Функции для формирования выходной информации.
"""

import textwrap
import time
from decimal import ROUND_HALF_UP, Decimal

import pyshorteners
from prettytable import ALL, PrettyTable

from collectors.models import LocationInfoDTO


class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    async def render(self) -> PrettyTable:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """
        table = PrettyTable(
            ["Type", "Info"], hrules=ALL, vrules=ALL, header_style="upper"
        )
        for key, value in {
            "Страна": self.location_info.location.name,
            "Столица": self.location_info.location.capital,
            "Регион": self.location_info.location.subregion,
            "Языки": (await self._format_languages()),
            "Население страны": f"{await self._format_population()} чел.",
            "Курсы валют": (await self._format_currency_rates()),
            "Информация о погоде": (
                f"температура: {self.location_info.weather.temp} °C, "
                f"описание: {self.location_info.weather.description}, "
                f"видимость (м): {self.location_info.weather.visibility}, "
                f"скорость ветра (м/с): {self.location_info.weather.wind_speed}."
            ),
            "Площадь страны": f"{self.location_info.location.area} кв. м.",
            "Координаты столицы": (await self._get_city_coordinates()),
            "Текущее время в столице": (await self._get_city_time_by_timezone()),
        }.items():
            table.add_row([key, value])
        table.max_width = 40

        return table

    async def top_3_news_in_country(self) -> PrettyTable | None:
        table = PrettyTable(
            ["author", "title", "url"],
            hrules=ALL,
            vrules=ALL,
            header_style="upper",
        )
        if self.location_info.news is None:
            return None
        # вытаскиваем три самые свежие новости
        for new in self.location_info.news[:3]:
            shortener = pyshorteners.Shortener()
            # Сокращаем длинную URL
            short_url = shortener.tinyurl.short(new.url)
            table.add_row([new.author, textwrap.fill(new.title, width=20), short_url])

        return table

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )

    async def _get_city_coordinates(self) -> str:
        """
        Получение географических координат столицы.

        :return:
        """
        return f"широта: {self.location_info.capital.latitude}, долгота: {self.location_info.capital.longitude}"

    async def _get_city_time_by_timezone(self) -> str:
        """
        Получение времени в городе по его часовому поясу.

        :return:
        """

        timezone = self.location_info.weather.timezone  # в секундах

        return f"{time.ctime(time.time() + (timezone - 10800))} (UTC+{timezone / 3600})"
