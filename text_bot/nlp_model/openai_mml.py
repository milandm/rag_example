import openai
from openai import OpenAI

from typing import Union, Generator, Any
from text_bot.nlp_model.mml_model import MmlModel

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

EMBEDDING_MODEL = "text-embedding-3-small"
# LLM_MODEL = "gpt-3.5-turbo"
# LLM_MODEL = "gpt-4"
LLM_MODEL ="gpt-4o"

IMAGE_MODEL = "dall-e-3"
IMAGE_SIZE = "1024x1024"
IMAGE_QUALITY = "standard"

# MAX_CHARACTERS = MAX_TOKENS x 4
# MAX_TOKENS = 4095
# MAX_TOKENS = 8192
MAX_TOKENS = 4096
# MAX_TOKENS = 1024

class OpenaiMml(MmlModel):

    VECTOR_PARAMS_SIZE = 1536
    # VECTOR_PARAMS_SIZE = 3072

    def __init__(self):

        openai.api_type = OPENAI_API_TYPE
        openai.api_key = OPENAI_API_KEY
        openai.api_version = OPENAI_API_VERSION
        openai.azure_endpoint = AZURE_OPENAI_ENDPOINT
        self.llm = ChatOpenAI(temperature=0, model_name=LLM_MODEL)
        self.open_ai_embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)


    def get_embedding(self, text):
        return self.open_ai_embeddings.embed_query(text)

    def generate_image(self, image_description_prompt):
        response = openai.images.generate(
            model=IMAGE_MODEL,
            prompt=image_description_prompt,
            size=IMAGE_SIZE,
            quality=IMAGE_QUALITY,
            n=1,
        )
        return response

    def get_embeddings(self, sentences: List[str]) -> List[List[float]]:
        return self.open_ai_embeddings.embed_documents(sentences)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Call the base embeddings."""
        return self.base_embeddings.embed_documents(texts)

    def combine_embeddings(self, embeddings: List[List[float]]) -> List[float]:
        """Combine embeddings into final embeddings."""
        return list(np.array(embeddings).mean(axis=0))

    def embed_query(self, text: str) -> List[float]:
        """Generate a hypothetical document and embedded it."""
        var_name = self.llm_chain.input_keys[0]
        result = self.llm_chain.generate([{var_name: text}])
        documents = [generation.text for generation in result.generations[0]]
        embeddings = self.embed_documents(documents)
        return self.combine_embeddings(embeddings)

    def _filter_similar_embeddings(
            embedded_documents: List[List[float]], similarity_fn: Callable, threshold: float
    ) -> List[int]:
        """Filter redundant documents based on the similarity of their embeddings."""
        similarity = np.tril(similarity_fn(embedded_documents, embedded_documents), k=-1)
        redundant = np.where(similarity > threshold)
        redundant_stacked = np.column_stack(redundant)
        redundant_sorted = np.argsort(similarity[redundant])[::-1]
        included_idxs = set(range(len(embedded_documents)))
        for first_idx, second_idx in redundant_stacked[redundant_sorted]:
            if first_idx in included_idxs and second_idx in included_idxs:
                # Default to dropping the second document of any highly similar pair.
                included_idxs.remove(second_idx)
        return list(sorted(included_idxs))
