from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import GigaChat
from aiogram.types import Message
from dotenv import load_dotenv
from retriveval import Augmentations

load_dotenv()


class TextGen(object):
    def __init__(self, credentials, ssl_cert, scope, profanity):
        self.chat = GigaChat(
            credentials=credentials,
            verify_ssl_certs=ssl_cert,
            scope=scope,
            profanity=profanity,
        )
        self.augmentation = Augmentations("documents", "embeding_store")

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
                    вопросы, касающиеся РГГМУ. Если контекст большой, то
                    используй его по максимуму, но не теряй сути. 
                    При ответе на вопросы общайся в деловом стиле и пиши
                    только по существу. """
                ),
                HumanMessage(
                    content=prompt.format(
                        subject=self.augmentation.augment_prompt(message)
                    )
                ),
            ]
        )

        return output.content


# talkbox = TextGen("OGM3MzZmZDAtNzliNi00OGQ2LTliMzktZWUwZTk1MDU2NGNjOmExYzgyMmVkLThmNjMtNGU3MC1hZWZlLTc5NDM1NWRiNDkzMA==", False, "GIGACHAT_API_PERS", True)
# a = talkbox.answer("Где проходит практика у гидрологов?")
# print(a)
