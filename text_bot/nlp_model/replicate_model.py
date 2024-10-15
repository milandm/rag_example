import replicate
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Callable
import logging
from text_bot.utils import retry
from text_bot.nlp_model.nlp_model import NlpModel


import random
import re
import replicate

from text_bot.nlp_model.config import REPLICATE_API_TOKEN

from collections.abc import Generator
from custom_logger.universal_logger import UniversalLogger

from text_bot.nlp_model.rag.llama_structured_prompt_creator import LlamaStructuredPromptCreator, STRUCTURED_OUTPUT_SYSTEM_PROMPT

import json

# import replicate
#
# input = {
#     "top_p": 0.9,
#     "prompt": "Paper title: A proof that drinking coffee causes supernovas\n\nIn this essay, I will",
#     "min_tokens": 0,
#     "temperature": 0.6,
#     "presence_penalty": 1.15
# }
#
# for event in replicate.stream(
#     "meta/meta-llama-3-70b",
#     input=input
# ):
#     print(event, end="")


EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
# LLM_MODEL = "gpt-3.5-turbo"
# LLM_MODEL = "gpt-4"
LLM_MODEL_70 ="meta/meta-llama-3-70b"
LLM_MODEL_70_INSTRUCT = "meta/meta-llama-3.1-70b-instruct"
META_LLAMA_3_1_405b_INSTRUCT = "meta/meta-llama-3.1-405b-instruct"
LLM_MODEL = "llama-3-1"
LLM_MODEL_STRUCTURED_OUTPUT = "gpt-4o-2024-08-06"
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser



class ReplicateModel(NlpModel):

    VECTOR_PARAMS_SIZE = 384  # For 'all-MiniLM-L6-v2' model

    def __init__(self):
        self.model_name = LLM_MODEL
        # Initialize the embeddings model
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.llama_structured_prompt_creator = LlamaStructuredPromptCreator()

        # Get the latest version of the model
        # self.model = replicate.models.get(self.model_name)
        # self.version = self.model.versions.list()[0]

        # # Initialize the Replicate client
        # self.replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)
        #
        # # Load the Llama 3.1 model
        # self.model = self.replicate_client.models.get(LLM_MODEL)

        # self.replicate_stream = replicate.stream(
        #         "meta/meta-llama-3-70b",
        #         input=input
        #     )

        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)




    def get_embedding(self, text: str) -> List[float]:
        """Generate embeddings for a single text input."""
        return self.embedding_model.encode(text).tolist()



    @retry(max_retries=3, initial_delay=1, backoff=2)
    def send_prompt(self, prompt: str, max_length: int = 512, temperature: float = 0.6, top_p: float = 0.9, **kwargs) -> str:
        """Send a prompt to the LLaMA model and get the generated text."""
        input = {
            "top_p": 0.9,
            "prompt": prompt,
            "min_tokens": 0,
            "temperature": 0.6,
            "presence_penalty": 1.15
        }

        output = replicate.run(
            META_LLAMA_3_1_405b_INSTRUCT,
            input=input
        )
        print("".join(output))
        return output


    @retry(max_retries=3, initial_delay=1, backoff=2)
    def predict_v3(self, prompt: str, max_length: int = 512, temperature: float = 0.6, top_p: float = 0.9,
                **kwargs) -> str:
        """Send a prompt to the LLaMA model and get the generated text."""
        input = {
            "top_p": top_p,
            "prompt": prompt,
            "min_tokens": 0,
            "temperature": temperature,
            "presence_penalty": 1.15
        }

        output = replicate.run(
            "meta/meta-llama-3-70b",
            input=input
        )

        print(output)
        return output


    @retry(max_retries=3, initial_delay=1, backoff=2)
    def predict_v1(self, prompt: str, max_length: int = 512, temperature: float = 0.6, top_p: float = 0.9, **kwargs) -> str:
        """Send a prompt to the LLaMA model and get the generated text."""
        input = {
            "top_p": 0.9,
            "prompt": prompt,
            "min_tokens": 0,
            # "max_tokens": 0,
            "temperature": 0.6,
            "presence_penalty": 1.15
        }

        prediction = replicate.predictions.create(
            model="meta/meta-llama-3-70b",
            input=input
        )
        print("".join(prediction))
        return prediction


    @retry(max_retries=3, initial_delay=1, backoff=2)
    def predict(self, prompt: str, max_length: int = 512, temperature: float = 0.6, top_p: float = 0.9,
                **kwargs) -> str:
        """Send a prompt to the LLaMA model and get the generated text."""
        input = {
            "top_p": top_p,
            "prompt": prompt,
            "min_tokens": 0,
            "temperature": temperature,
            "presence_penalty": 1.15
        }

        prediction = None

        try:
            prediction = replicate.predictions.create(
                model=META_LLAMA_3_1_405b_INSTRUCT,
                input=input
            )

            # Wait for the prediction to complete
            prediction.wait()
        except Exception as e:
            self.logger.error(e)

        # Check if the prediction succeeded
        if prediction and prediction.status == "succeeded":
            output = prediction.output
        else:
            raise Exception(f"Prediction failed: {prediction.error}")

        # Print and return the output
        print(output)
        return output





    def get_embeddings(self, sentences: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of sentences."""
        return [embedding.tolist() for embedding in self.embedding_model.encode(sentences)]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Alias for get_embeddings."""
        return self.get_embeddings(texts)

    def combine_embeddings(self, embeddings: List[List[float]]) -> List[float]:
        """Combine a list of embeddings into a single embedding."""
        return list(np.mean(embeddings, axis=0))

    def embed_query(self, text: str) -> List[float]:
        """Embed a query text."""
        return self.get_embedding(text)

    def _filter_similar_embeddings(
            self, embedded_documents: List[List[float]], similarity_fn: Callable, threshold: float
    ) -> List[int]:
        """Filter redundant documents based on the similarity of their embeddings."""
        embeddings_array = np.array(embedded_documents)
        similarity_matrix = similarity_fn(embeddings_array, embeddings_array)
        # Zero out the upper triangle to ignore duplicate pairs
        similarity_matrix = np.tril(similarity_matrix, k=-1)
        redundant_pairs = np.argwhere(similarity_matrix > threshold)
        included_idxs = set(range(len(embedded_documents)))
        for idx_pair in redundant_pairs:
            idx1, idx2 = idx_pair
            if idx2 in included_idxs:
                included_idxs.remove(idx2)
        return sorted(included_idxs)



    def send_prompt_structured_output(self, system_msg: str = STRUCTURED_OUTPUT_SYSTEM_PROMPT,
                                      user_prompt: str = "",
                                      structured_output_model: BaseModel = None):
        self.logger.info("send_prompt_structured_output")
        structured_prompt = self.llama_structured_prompt_creator.get_generate_json_structured_output_prompt(
            system_msg = system_msg,
            user_prompt = user_prompt,
            structured_output_model = structured_output_model )
        self.logger.info("send_prompt_structured_output structured_prompt: " + str(structured_prompt))
        output = self.send_prompt(prompt=structured_prompt)
        return output


    def predict_structured_output(self, system_msg: str = STRUCTURED_OUTPUT_SYSTEM_PROMPT,
                                      user_prompt: str = "",
                                      structured_output_model: BaseModel = None):
        self.logger.info("send_prompt_structured_output")

        # Define the parser using the Pydantic model we defined earlier
        self.output_parser = PydanticOutputParser(pydantic_object=structured_output_model)

        structured_prompt = self.llama_structured_prompt_creator.get_generate_json_structured_output_prompt(
            system_msg = system_msg,
            user_prompt = user_prompt,
            structured_output_model = structured_output_model )
        self.logger.info("send_prompt_structured_output structured_prompt: "+str(structured_prompt))
        output = self.send_prompt(prompt=structured_prompt)

        self.logger.info("send_prompt_structured_output output: " + str(output))
        self.logger.info("send_prompt_structured_output output object type: " + str(type(output)))

        if not isinstance(output, str):
            # output = json.dumps(output)
            try:
                output = self.output_parser.parse(output)
            except Exception as e:
                print(f"Failed to parse output: {e}")

        return output