import logging
import asyncio
import sys
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold, hlink
from dotenv import load_dotenv
from os import getenv
from text_generator import TextGen
from speech2text import recognize_speech
from videohandler import video_handler
from time import sleep

load_dotenv()

logs = "messages.log"
talkbox = TextGen(getenv("WORK_CREDENTIAL"), False, getenv("WORK_SCOPE"), False)
TOKEN = getenv("TELEGRAM_TOKEN")
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
video_name = "video.mp4"
dummy_message = "Ищу ответ..."
stub = hbold("Бот работает в тестовом режиме – не все ответы могут быть достоверными")


# Start message
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This is handler for command `/start`
    """
    await message.answer(
        f"Привет, {hbold('студент')}\n\nПеред тобой бот-асситент ИИСИГТ,\
 подготовленный {hlink('мной', 'https://github.com/yaz0p')} к качестве\
 выпускной квалификационной работы\n\nДанный бот позволяет осуществлять\
 удобную навигацию внутри университета и отвечает на не самые очевидные\
 вопросы. \n\nБот работает на основе большой языковой модели, а\
 информацию о внутренних источниках получает благодаря {hbold('RAG')}.\
 Возможно, я прикреплю сюда git репозиторий с реализацией проекта,\
 чтобы студенты могли изучить работу данного ассистента и/или дополнить\
 его своими идеями.\n\n\
Пример того, что ты можешь спросить:\n- Адрес какого либо-корпуса\n\
- Номер приемной комиссии\n- Как поступить в ВУЦ\n- Время приема ректората\
 - Информацию о заселении и медкомиссии\n"
    )
    sleep(2)
    await message.answer(
        f"Для получения инструкции о взаимодействии с\
        ассистентом нажмите /help\n\n\
{hbold('Внимание, все сообщения логгируются!')}"
    )


@dp.message(F.text, Command("help"))
async def help_msg(message: Message):
    await message.answer(
        f"Бот распознает как текстовые сообщения, так и видео-\
 / голосовые сообщения.\n\nБот позволяет неявно искать информацию.\
 Например, можно спросить как номер приемки или номер приемной комиссии, так и\
 как связаться с приемной комиссей.\n\nПри записи голосовых сообщений следует\
 произносить слова членораздельно, чтобы сообщение могло корректно\
 распознаться. Так же следует корректно задавать свои вопросы."
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


# Main chapter with retrieval
@dp.message(F.text)
async def chat_handler(message: Message) -> None:
    if "расписание" in str(message).lower():
        await message.answer(
            "Расписание можно найти по данной ссылке:\
 https://www.rshu.ru/university/stud/"
        )
    else:
        try:
            msg = await message.answer(dummy_message)
            talkbox_msg = talkbox.answer(message.text)
            await message.answer(f"{talkbox_msg}\n\n{stub}")
            await msg.delete()
            with open(logs, "a") as log:
                log_msg = f"ID: {message.from_user.id} | Username: {message.from_user.full_name} | Message: {message.text} | Answer: {talkbox_msg}\n\n"
                log.write(log_msg)
                print(log_msg)

        except TypeError:
            await message.answer(
                "Что-то пошло не так! Сообщил разработчку о произошедшей неполадке!"
            )
            with open(logs, "a") as log:
                log.write(
                    f"ID: {message.from_user.id} | Username: {message.from_user.full_name} | ErrorMessage\n\n"
                )


@dp.message(F.voice)
async def audio_handler(message: Message) -> None:
    voice_message = await bot.get_file(message.voice.file_id)
    voice_message = voice_message.file_path
    await bot.download_file(voice_message, "voice.wav")
    with open("voice.wav", "rb") as voice_message:
        text = recognize_speech(voice_message)
        if "расписание" in text.lower():
            await message.answer(
                "Расписание можно найти по данной ссылке: https://www.rshu.ru/university/stud/"
            )
        else:
            msg = await message.answer(dummy_message)
            talkbox_msg = talkbox.answer(text)
            await message.answer(f"{talkbox.answer(text)}\n\n{stub}")
            await msg.delete()
            with open(logs, "a") as log:
                log_msg = f"ID: {message.from_user.id} | Username: {message.from_user.full_name} | Message: {text} | Answer: {talkbox_msg}\n\n"
                log.write(log_msg)
                print(log_msg)


@dp.message(F.video_note)
async def videomessage_handler(message: Message) -> None:
    voice_message = await bot.get_file(message.video_note.file_id)
    voice_message = voice_message.file_path
    await bot.download_file(voice_message, video_name)
    video_handler(video_name)
    with open("voice.wav", "rb") as voice_message:
        text = recognize_speech(voice_message)
        msg = await message.answer(dummy_message)
        talkbox_msg = talkbox.answer(text)
        await message.answer(f"{talkbox_msg}\n\n{stub}")
        await msg.delete()
        with open(logs, "a") as log:
            log_msg = f"ID: {message.from_user.id} | Username: {message.from_user.full_name} | Message: {text} | Answer: {talkbox_msg}\n\n"
            log.write(log_msg)
            print(log_msg)


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
