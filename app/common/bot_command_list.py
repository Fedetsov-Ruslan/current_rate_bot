from aiogram.types import BotCommand


private = [
    BotCommand(command="exchange", description="Конвертация валют в виде '/exchange <валюта1> <валюта2> <количество>'"),
    BotCommand(command="rates", description="Показывает список валют"),
    BotCommand(command="start", description="start"),
]