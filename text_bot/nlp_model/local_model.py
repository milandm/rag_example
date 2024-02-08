from sentence_transformers import SentenceTransformer
import torch

import numpy as np
from numpy import ndarray
from tqdm import tqdm
from text_bot.nlp_model.nlp_model import NlpModel
from typing import Union, Generator, Any
from text_bot.nlp_model.openai_model import OpenaiModel


SENTENCE_TRANSFORMER_NLP_MODEL = "msmarco-MiniLM-L-6-v3"
CUDA = "cuda"
MPS = "mps"
CPU = "cpu"

class LocalModel(NlpModel):

    VECTOR_PARAMS_SIZE = 384

    def __init__(self):
        self.model = SentenceTransformer(
            SENTENCE_TRANSFORMER_NLP_MODEL,
            device=CUDA
            if torch.cuda.is_available()
            else MPS
            if torch.backends.mps.is_available()
            else CPU,
        )
        self.nlp_prompt_model = OpenaiModel()

    def get_embeddings(self, sentences: list[str]) -> ndarray:

        vectors = []
        batch_size = 512
        batch = []

        for doc in tqdm(sentences):
            batch.append(doc)

            if len(batch) >= batch_size:
                vectors.append(self.model.encode(batch))
                batch = []

        if len(batch) > 0:
            vectors.append(self.model.encode(batch))
            batch = []

        vectors = np.concatenate(vectors)

        return vectors

    def get_embedding(self, text:str):
        self.model.encode(text)


    def send_prompt( self, system_msg:str, user_prompt:str ):
        return self.nlp_prompt_model.send_prompt(system_msg, user_prompt)