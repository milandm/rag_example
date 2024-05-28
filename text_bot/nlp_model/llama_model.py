from sentence_transformers import SentenceTransformer
import torch

import numpy as np
from numpy import ndarray
from tqdm import tqdm
from text_bot.nlp_model.nlp_model import NlpModel
from typing import Union, Generator, Any, List
# from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.llms.ollama import Ollama

# # Llama 2 models are 4096
#
#
# llm = Llama(model_path="./models/llama-2-7b-chat.ggmlv3.q2_K.bin",
#             n_ctx=1024, n_batch=128, verbose=False)
# instruction = input("User: ")
# # put together the instruction in the prompt template for Orca models
# prompt = f"[INST] <<SYS>><</SYS>>\n{instruction} [/INST]"
# output = llm(prompt,temperature  = 0.7, max_tokens=1024, top_k=20, top_p=0.9,
#             repeat_penalty=1.15)
# res = output['choices'][0]['text'].strip()
# print('Llama2-7b: ' + res)
#
#
# llm = Llama(model_path="./models/orca-mini-3b.ggmlv3.q4_1.bin", n_ctx=512, n_batch=32, verbose=False)
# instruction = input("User: ")
# # put together the instruction in the prompt template for Orca models
# system = 'You are an AI assistant that follows instruction extremely well. Help as much as you can.'
# prompt = f"### System:\n{system}\n\n### User:\n{instruction}\n\n### Response:\n"
# output = llm(prompt,temperature  = 0.7,max_tokens=512,top_k=20, top_p=0.9,
#                     repeat_penalty=1.15)
# res = output['choices'][0]['text'].strip()
#
#
#
# llm.create_chat_completion(
#     messages = [
#         {"role": "system", "content": "You are an assistant who perfectly describes images."},
#         {
#             "role": "user",
#             "content": [
#                 {"type": "image_url", "image_url": {"url": "https://.../image.png"}},
#                 {"type" : "text", "text": "Describe this image in detail please."}
#             ]
#         }
#     ]
# )



# from llama_cpp import Llama
# llm = Llama(model_path="path/to/llama-2/llama-model.gguf", chat_format="llama-2")
# llm.create_chat_completion(
#       messages = [
#           {"role": "system", "content": "You are an assistant who perfectly describes images."},
#           {
#               "role": "user",
#               "content": "Describe this image in detail please."
#           }
#       ]
# )

import os
from huggingface_hub import hf_hub_download

SENTENCE_TRANSFORMER_NLP_MODEL = "msmarco-MiniLM-L-6-v3"
CUDA = "cuda"
MPS = "mps"
CPU = "cpu"

class LLamaModel(NlpModel):

    VECTOR_PARAMS_SIZE = 384

    def __init__(self):



        # self.embedding_model = HuggingFaceEmbedding(
        #     model_name=embedding_hf_model_name,
        #     cache_folder=str(models_cache_path),
        # )
        # self.check_and_download_model()
        self.nlp_prompt_model = \
            Ollama(model_path="./models/llama-2-7b-chat.ggmlv3.q2_K.bin",
                    n_ctx=1024,
                    n_batch=128,
                    verbose=False)

        self.model = SentenceTransformer(
            SENTENCE_TRANSFORMER_NLP_MODEL,
            device=CUDA
            if torch.cuda.is_available()
            else MPS
            if torch.backends.mps.is_available()
            else CPU,
        )

    def download_model_if_not_exists(self, repo_id, filename, save_path):
        """
        Checks if a model file already exists locally. If not, downloads it from Hugging Face.

        :param repo_id: Repository ID on Hugging Face (e.g., 'bert-base-uncased').
        :param filename: Name of the file to download (e.g., 'pytorch_model.bin').
        :param save_path: Local path to save the file.
        :return: Path to the local model file.
        """

        # Full path for the file
        full_path = os.path.join(save_path, filename)

        # Check if the file already exists
        if not os.path.exists(full_path):
            print(f"Downloading {filename} from {repo_id}...")
            model_file = hf_hub_download(repo_id, filename, cache_dir=save_path)
            print(f"Model downloaded and saved to {model_file}")
        else:
            print(f"Model file {filename} already exists at {full_path}")

        return full_path

    def check_and_download_model(self):
        # Example usage
        repo_id = "TheBloke/Llama-2-7B-Chat-GGML"  # Replace with the actual repository ID
        filename = "Llama-2-7B-Chat-GGML"  # Replace with the actual file name
        save_path = "./models"  # Replace with your desired save path

        model_path = self.download_model_if_not_exists(repo_id, filename, save_path)

    def get_embeddings(self, sentences: List[str]) -> ndarray:

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

        # instruction = input("User: ")
        # # put together the instruction in the prompt template for Orca models
        # prompt = f"[INST] <<SYS>><</SYS>>\n{instruction} [/INST]"
        response = self.nlp_prompt_model.create_chat_completion(
                                        messages=[{"role": "system", "content": system_msg},
                                                  {"role": "user", "content": user_prompt}],
                                       temperature=0,
                                       max_tokens=1024,
                                       top_k=1,
                                       top_p=1,
                                       repeat_penalty=0)

        # self.nlp_prompt_model.create_chat_completion(
        #     messages=[{"role": "system", "content": system_msg},
        #               {"role": "user", "content": user_prompt}]
        # )

        return response