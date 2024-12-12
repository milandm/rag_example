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

from custom_logger.universal_logger import UniversalLogger

PERPLEXITY_API_KEY = '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'


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



class PerplexityApi(NlpModel):

    VECTOR_PARAMS_SIZE = 1536
    # VECTOR_PARAMS_SIZE = 3072

    def __init__(self):
        self.client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)


    def get_embedding(self, text):
        return None

    @retry(max_retries=3, initial_delay=1, backoff=2)
    def send_prompt( self, system_msg:str, user_prompt:str ):
        # chat completion without streaming
        response = self.client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online",
            messages=[{"role": "system", "content": system_msg},
                      {"role": "user", "content": user_prompt}],
            temperature=0,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0
        )
        return response


    @retry(max_retries=3, initial_delay=1, backoff=2)
    def send_prompt_structured_output(self, system_msg: str,
                                      user_prompt: str,
                                      structured_output_model: BaseModel):
        return None


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



# client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
#
# # chat completion without streaming
# response = client.chat.completions.create(
#     model="llama-3.1-sonar-large-128k-online",
#     messages=messages,
# )
# print(response)
#
# # chat completion with streaming
# response_stream = client.chat.completions.create(
#     model="llama-3.1-sonar-large-128k-online",
#     messages=messages,
#     stream=True,
# )
# for response in response_stream:
#     print(response)