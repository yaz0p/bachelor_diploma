from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import GigaChat
from aiogram.types import Message
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class TextGen(object):
    def __init__(self, credentials, ssl_cert, scope, profanity):
        self.chat = GigaChat(
            credentials=credentials,
            verify_ssl_certs=ssl_cert,
            scope=scope,
            profanity=profanity,
        )

    def answer(self, message: Message) -> None:
        prompt = PromptTemplate(
            template="Ответь на поставленный вопрос: {subject}",
            input_variables=["subject"],
        )

        output = self.chat(
            [
                SystemMessage(
                    content="""Ты профессиональный ассистент Российского
                    государственного гидрометеорологического университета,
                    который помогает студентам и преподавателям решать их
                    проблемы: навигация внутри университета, ответ на общие
                    вопросы, касающиеся РГГМУ. При ответе на вопросы общайся
                    в деловом стиле и пиши только по существу."""
                ),
                HumanMessage(content=prompt.format(subject=message)),
            ]
        )

        return output.content


talkbox = TextGen(getenv("CREDENTIAL"), False, getenv("SCOPE"), True)
# a = talkbox.answer("Привет, что ты умеешь?")
# print(a)
# print(type(a))
