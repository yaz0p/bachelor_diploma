import logging
import asyncio
import sys
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.types import Message, BotCommand
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold, hlink
from dotenv import load_dotenv
from os import getenv
from text_generator import TextGen

load_dotenv()

talkbox = TextGen(getenv("CREDENTIAL"), False, getenv("SCOPE"), True)
TOKEN = getenv("TELEGRAM_TOKEN")
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


# Start message
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This is handler for command `/start`
    """
    await message.answer(
        f"Привет, {hbold('студент')}\n\nПеред тобой бот-асситент РГГМУ, подготовленный к качестве выпускной квалификационной работы {hlink('мной', 'https://github.com/yaz0p')}\n\nДанный бот позволяет осуществлять удобную навигацию внутри университета и отвечает на не самые очевидные вопросы. \n\nБот работает на основе большой языковой модели, а так же дообучения при помощи RAG. Возможно, я прикреплю сюда git репозиторий с реализацией проекта, чтобы студенты могли изучить работу данного ассистента или дополнить его своими идеями."
    )


# Menu button
async def bot_menu():
    bot_command = [
        BotCommand(command="/start", description="Получить информацию о боте"),
        BotCommand(
            command="/help",
            description="Инструкция по правильному взаимодействую с ботом",
        ),
    ]

    await bot.set_my_commands(bot_command)

@dp.message()
async def chat_handler(message: Message) -> None:
    try:
        await message.answer(talkbox.answer(message))
    except TypeError:
        await message.answer(
            "Что-то пошло не так! Сообщил разработчку о произошедшей неполадке!"
        )


async def main() -> None:
    """
    Init bot instance

    Startup create navigation menu

    Start pooling start bot
    """
    dp.startup.register(bot_menu)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
