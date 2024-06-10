"""
Функции для формирования выходной информации.
"""

import time
from decimal import ROUND_HALF_UP, Decimal

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

    async def render(self) -> tuple[str, ...]:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """

        return (
            f"Страна: {self.location_info.location.name}",
            f"Столица: {self.location_info.location.capital}",
            f"Регион: {self.location_info.location.subregion}",
            f"Языки: {await self._format_languages()}",
            f"Население страны: {await self._format_population()} чел.",
            f"Курсы валют: {await self._format_currency_rates()}",
            "Информация о погоде: ",
            f"\tтемпература: {self.location_info.weather.temp} °C, ",
            f"\tописание: {self.location_info.weather.description}, ",
            f"\tвидимость (м): {self.location_info.weather.visibility}, ",
            f"\tскорость ветра (м/с): {self.location_info.weather.wind_speed}",
            f"Площадь страны: {self.location_info.location.area} кв. м.",
            f"Координаты столицы: {await self._get_city_coordinates()}",
            f"Текущее время в столице: {await self._get_city_time_by_timezone()}",
        )

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
