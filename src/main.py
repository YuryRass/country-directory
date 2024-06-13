"""
Запуск приложения.
"""

import asyncclick as click

from reader import Reader
from renderer import Renderer


@click.command()
@click.option(
    "--location",
    "-l",
    "location",
    type=str,
    help="Страна и/или город",
    prompt="Страна и/или город",
)
async def process_input(location: str) -> None:
    """
    Поиск и вывод информации о стране, погоде и курсах валют.

    :param str location: Страна и/или город
    """

    location_info = await Reader().find(location)
    if location_info:
        rend = Renderer(location_info)
        main_info = await rend.render()
        news = await rend.top_3_news_in_country()

        click.secho("\nВывод информации в стране:", fg="magenta")
        click.secho(main_info, fg="green")
        if news is not None:
            click.secho("\nПоследние три новости в стране:", fg="magenta")
            click.secho(news, fg="blue")
        else:
            click.secho("Новостей в стране нет!", fg="yellow")
    else:
        click.secho("Информация отсутствует.", fg="red")


if __name__ == "__main__":
    # запуск обработки входного файла
    # pylint: disable=E1120
    process_input(_anyio_backend="asyncio")
