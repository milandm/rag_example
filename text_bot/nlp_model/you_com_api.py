from openai import OpenAI


import openai
from openai import OpenAI

from typing import Union, Generator, Any
from text_bot.nlp_model.nlp_model import NlpModel

from text_bot.nlp_model.config import (
    OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    OPENAI_API_TYPE,
    OPENAI_API_VERSION
)

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from typing import List, Callable
import numpy as np
from text_bot.utils import retry
from pydantic import BaseModel
import requests

YOU_COM_API_KEY = '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'

YOU_COM_SEARCH_API_KEY = 'eb2b5abc-7269-42a9-886c-b3c5b9b1f1a1<__>1QPkeXETU8N2v5f4c75caNnV'


LLM_MODEL = "llama-3.1-sonar-large-128k-online"
LLM_MODEL_HUGE = 'llama-3.1-sonar-huge-128k-online'

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        ),
    },
    {
        "role": "user",
        "content": (
            "How many stars are in the universe?"
        ),
    },
]





import os

from langchain.retrievers.you import YouRetriever
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from custom_logger.universal_logger import UniversalLogger


os.environ["YDC_API_KEY"] = YOU_COM_API_KEY
# os.environ["OPENAI_API_KEY"] = "YOUR OPENAI API KEY"

LLM_MODEL ="gpt-4o"
LLM_MODEL_STRUCTURED_OUTPUT = "gpt-4o-2024-08-06"


class YouComApi(NlpModel):

    VECTOR_PARAMS_SIZE = 1536
    # VECTOR_PARAMS_SIZE = 3072

    def __init__(self):
        self.headers = {"X-API-Key": YOU_COM_API_KEY}
        self.you_retriever = YouRetriever()
        self.retrieval_qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(model=LLM_MODEL),
                                         chain_type="stuff",
                                         retriever=self.you_retriever)
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)


    def get_embedding(self, text):
        return None

    @retry(max_retries=3, initial_delay=1, backoff=2)
    def send_prompt(self, system_msg:str, user_prompt:str ):
        # chat completion without streaming
        response = self.query_web_llm(user_prompt)
        self.logger.info("You com response: " + str(response))
        # response = self.retrieval_qa.run(user_prompt)

        return response

    @retry(max_retries=3, initial_delay=1, backoff=2)
    def send_search_query(self, search_query:str ):
        # chat completion without streaming
        response = self.get_ai_snippets_for_query(search_query)
        return response

    @retry(max_retries=3, initial_delay=1, backoff=2)
    def send_prompt_structured_output(self, system_msg: str,
                                      user_prompt: str,
                                      structured_output_model: BaseModel):
        # chat completion without streaming
        response = self.query_web_llm(user_prompt)
        self.logger.info("You com response: " + str(response))
        # response = self.retrieval_qa.run(user_prompt)

        return response


    def get_embeddings(self, sentences: List[str]) -> List[List[float]]:
        return None

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Call the base embeddings."""
        return None

    def combine_embeddings(self, embeddings: List[List[float]]) -> List[float]:
        """Combine embeddings into final embeddings."""
        return None

    def embed_query(self, text: str) -> List[float]:
        return None

    def _filter_similar_embeddings(
            embedded_documents: List[List[float]], similarity_fn: Callable, threshold: float
    ) -> List[int]:
        return None


    def query_web_llm(self, query):
        params = {"query": query}
        return requests.get(
            f"https://api.ydc-index.io/rag?query={query}",
            params=params,
            headers=self.headers)


    def query_web_llm_structured(self, query):
        params = {"query": query}
        return requests.get(
            f"https://api.ydc-index.io/rag?query={query}",
            params=params,
            headers=self.headers,
        ).json()

    def get_ai_snippets_for_query(self, query):
        params = {"query": query}
        return requests.get(
            f"https://api.ydc-index.io/search",
            params=params,
            headers=self.headers,
        ).json()
