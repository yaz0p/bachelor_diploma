import logging
import asyncio
import sys
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold, hlink

TOKEN = "6981508379:AAHKYOzmf5jBxyeAuUM83N0xEaNgaE-CpX0"
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This is handler for command `/start`
    """
    await message.answer(f"Привет, {hbold('студент')}\n\nПеред тобой бот-асситент РГГМУ, подготовленный к качестве выпускной квалификационной работы {hlink('мной', 'https://github.com/yaz0p')}\n\nДанный бот позволяет осуществлять удобную навигацию внутри университета и отвечает на не самые очевидные вопросы. \n\nБот работает на основе большой языковой модели, а так же дообучения при помощи RAG. Возможно, я прикреплю сюда git репозиторий с реализацией проекта, чтобы студенты могли изучить работу данного ассистента или дополнить его своими идеями.")




async def main() -> None:
    """
    Initialize bot instance without modification
    """
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
