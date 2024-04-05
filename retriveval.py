from langchain_community.vectorstores import FAISS
from langchain.document_loaders.text import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import Any, Coroutine, List
from os import listdir
from itertools import chain


class HuggingFaceE5Embeddings(HuggingFaceEmbeddings):
    def embed_query(self, text: str) -> List[float]:
        text = f"query: {text}"
        return super().embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        texts = [f"passage: {text}" for text in texts]
        return super().embed_documents(texts)

    async def aembed_query(self, text: str) -> Coroutine[Any, Any, List[float]]:
        text = f"query: {text}"
        return await super().aembed_query(text)

    async def aembed_documents(
        self, texts: List[str]
    ) -> Coroutine[Any, Any, List[List[float]]]:
        texts = [f"passage: {text}" for text in texts]
        return await super().aembed_documents(texts)


class Augmentations(object):
    def __init__(self, path_to_docs: str, path_to_embedings: str) -> None:
        """
        Make path to documents
        """
        self.path_to_docs = path_to_docs
        self.path_to_embedings = path_to_embedings

    def _embedings_storage(self):
        embedding = HuggingFaceE5Embeddings(model_name="intfloat/multilingual-e5-base")
        docs_list = map(
            lambda x: self.path_to_docs + "/" + x, listdir(path=self.path_to_docs)
        )
        loader = map(lambda x: TextLoader(file_path=x), docs_list)
        documents = list(map(lambda x: x.load(), loader))

        documents = list(chain.from_iterable(documents))

        try:
            db = FAISS.load_local(
                folder_path=self.path_to_embedings,
                embeddings=embedding,
                allow_dangerous_deserialization=True,
            )
        except RuntimeError:
            db = FAISS.from_documents(documents, embedding)
            db.save_local(self.path_to_embedings)
        return db

    def augment_prompt(self, query: str, _embedings_storage=_embedings_storage):
        results = _embedings_storage(self).similarity_search(query, k=3)
        source_knowledge = "\n".join([x.page_content for x in results])
        augmented_prompt = f"""Используя предоставленный контекст ответь на следующий вопрос.

        Контекст:
        {source_knowledge}

        Вопрос: {query}"""
        return augmented_prompt
