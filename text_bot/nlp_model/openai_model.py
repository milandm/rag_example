import openai

from typing import Union, Generator, Any
from text_bot.nlp_model.nlp_model import NlpModel

from text_bot.nlp_model.config import (
    OPENAI_API_KEY,
)

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from typing import List, Callable
import numpy as np
from text_bot.utils import retry



SYSTEM_MSG = 'Ti si ekspert za zakone u oblasti klinickih istrazivanja.'
EMBEDDING_MODEL = "text-embedding-ada-002"
# LLM_MODEL = "gpt-3.5-turbo"
# LLM_MODEL = "gpt-4"
LLM_MODEL ="gpt-4-1106-preview"

# MAX_CHARACTERS = MAX_TOKENS x 4
# MAX_TOKENS = 4095
# MAX_TOKENS = 8192
MAX_TOKENS = 4096
# MAX_TOKENS = 1024

class OpenaiModel(NlpModel):

    VECTOR_PARAMS_SIZE = 1536

    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.llm = ChatOpenAI(temperature=0, model_name=LLM_MODEL)
        self.open_ai_embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)


    # Counter Hypothetical Document Embeddings (HyDE)
    # CREATE QUESTIONS FOR CONTEXT

    # def get_embedding(self, text, model="text-embedding-ada-002"):
    #     text = text.replace("\n", " ")
    #     return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']
    #

    # reformulate question to sound more as description of what to search for
    # using open ai request
    # use langchain.chains.qa_with_sources approach
    def get_embedding(self, text):
        return self.open_ai_embeddings.embed_query(text)

    @retry(max_retries=3, initial_delay=1, backoff=2)
    def send_prompt( self, system_msg:str, user_prompt:str ):

        response = openai.chat.completions.create(
            # model="gpt-3.5-turbo",
            model=LLM_MODEL,
            messages=[{"role": "system", "content": system_msg},
                       {"role": "user", "content": user_prompt}],
            max_tokens = MAX_TOKENS,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # {
        #     "model": "gpt-4",
        #     "messages": [
        #         {"role": "system", "content": "Set the behavior"},
        #         {"role": "assistant", "content": "Provide examples"},
        #         {"role": "user", "content": "Set the instructions"}
        #     ],
        #     "temperature": 0.05,
        #     "max_tokens": 256,
        #     "top_p": 1,
        #     "frequency_penalty": 0,
        #     "presence_penalty": 0
        # }

        # completion = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=prompt,
        #     max_tokens=1024,
        #     temperature=0.1,
        #     top_p=1,
        #     frequency_penalty=0,
        #     presence_penalty=0
        # )

        return response


    def get_embeddings(self, sentences: list[str]) -> list[list[float]]:
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





    # def send_prompt( self, user_prompt:str ) -> Union[Generator[Union[list, openai.OpenAIObject, dict], Any, None], list, OpenAIObject, dict]:
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "system", "content": SYSTEM_MSG},
    #                    {"role": "user", "content": user_prompt}],
    #         max_tokens=250,
    #         temperature=0.2,
    #     )
    #     return response
    #
    #     # # Define the system message
    #     # system_msg = 'You are a helpful assistant who understands data science.'
    #     #
    #     # # Define the user message
    #     # user_msg = 'Create a small dataset about total sales over the last year. The format of the dataset should be a data frame with 12 rows and 2 columns. The columns should be called "month" and "total_sales_usd". The "month" column should contain the shortened forms of month names from "Jan" to "Dec". The "total_sales_usd" column should contain random numeric values taken from a normal distribution with mean 100000 and standard deviation 5000. Provide Python code to generate the dataset, then provide the output in the format of a markdown table.'
    #     #
    #     # # Create a dataset using GPT
    #     # response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
    #     #                                         messages=[{"role": "system", "content": system_msg},
    #     #                                                   {"role": "user", "content": user_msg}])
    #
    #     # return {
    #     #     "response": response["choices"][0]["message"]["content"],
    #     #     "references": references,
    #     # }
    #
    # def get_embedding(self, text) -> Union[Generator[Union[list, openai.OpenAIObject, dict], Any, None], list, openai.OpenAIObject, dict]:
    #     # text = text.replace("\n", " ")
    #
    #     if isinstance(text, str):
    #         text = [text]
    #     embedding = openai.Embedding.create(input=text, model=EMBEDDING_MODEL)
    #
    #     embeddings = [row["embedding"]
    #         for row in embedding['data']
    #     ]
    #
    #     if len(embeddings) == 1:
    #         return embeddings[0]
    #
    #     return embeddings
    #
    #     # df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
    #     # df.to_csv('output/embedded_1k_reviews.csv', index=False)
    #
    #     # import pandas as pd
    #     #
    #     # df = pd.read_csv('output/embedded_1k_reviews.csv')
    #     # df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)
    #
    # def get_embeddings(self, sentences: list[str]) -> ndarray:
    #     vectors = []
    #     batch_size = 512
    #     batch = []
    #
    #     for doc in tqdm(sentences):
    #         batch.append(doc)
    #
    #         if len(batch) >= batch_size:
    #             vectors.append(self.get_embedding(batch))
    #             batch = []
    #
    #     if len(batch) > 0:
    #         vectors.append(self.get_embedding(batch))
    #         batch = []
    #
    #     vectors = np.concatenate(vectors)
    #
    #     return vectors