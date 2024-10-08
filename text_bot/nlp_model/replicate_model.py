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
LLM_MODEL = "llama-3-1"
LLM_MODEL_STRUCTURED_OUTPUT = "gpt-4o-2024-08-06"


class ReplicateModel(NlpModel):

    VECTOR_PARAMS_SIZE = 384  # For 'all-MiniLM-L6-v2' model

    def __init__(self):
        self.model_name = LLM_MODEL
        # Initialize the embeddings model
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
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
            "meta/meta-llama-3-70b",
            input=input
        )
        print("".join(output))
        return output


    @retry(max_retries=3, initial_delay=1, backoff=2)
    def predict(self, prompt: str, max_length: int = 512, temperature: float = 0.6, top_p: float = 0.9, **kwargs) -> str:
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


    def split_into_sentences(self, text):
        sentences = re.split(r'(?<=[.!?]) +', text)
        return sentences


    def create_cloze_test_samples(self, sentences, num_samples=100):
        samples = []
        for _ in range(num_samples):
            sentence = random.choice(sentences)
            words = sentence.split()
            if len(words) > 2:
                mask_idx = random.randint(0, len(words) - 1)
                masked_word = words[mask_idx]
                words[mask_idx] = '[MASK]'
                masked_sentence = ' '.join(words)
                samples.append((masked_sentence, masked_word))
        return samples


    def predict_masked_word(self, masked_sentence):
        # Prepare the prompt for Llama 3.1
        prompt = f"Fill in the blank: {masked_sentence}"

        # Generate prediction using the model
        output = self.predict(prompt=prompt)

        # Extract the predicted word from the model's output
        predicted_word = output.strip().split()[0]
        return predicted_word


    def evaluate_cloze_test(self, samples):
        correct = 0
        total = len(samples)
        for masked_sentence, actual_word in samples:
            predicted_word = self.predict_masked_word(masked_sentence)
            if predicted_word.lower() == actual_word.lower():
                correct += 1
        accuracy = correct / total * 100
        self.logger.info(f"Cloze Test Accuracy: {accuracy:.2f}%")

    def do_evaluation_test(self, corpus_text):
        # Example usage:
        sentences = self.split_into_sentences(corpus_text)
        cloze_samples = self.create_cloze_test_samples(sentences, num_samples=50)
        self.evaluate_cloze_test(cloze_samples)




    def create_next_word_prediction_samples(self, sentences, num_samples=100):
        samples = []
        for _ in range(num_samples):
            sentence = random.choice(sentences)
            words = sentence.split()
            if len(words) > 3:
                cut_off = random.randint(1, len(words) - 2)
                prompt = ' '.join(words[:cut_off])
                actual_next_word = words[cut_off]
                samples.append((prompt, actual_next_word))
        return samples


    def predict_next_word(self, prompt):
        # Prepare the prompt for Llama 3.1
        prompt = f"{prompt}"

        # Generate prediction using the model
        output = self.predict(prompt=prompt)

        # Extract the predicted word from the model's output
        predicted_word = output.strip().split()[0]
        return predicted_word


    def evaluate_next_word_prediction(self, samples):
        correct = 0
        total = len(samples)
        for prompt, actual_next_word in samples:
            predicted_word = self.predict_next_word(prompt)
            if predicted_word.lower() == actual_next_word.lower():
                correct += 1
        accuracy = correct / total * 100
        self.logger.info(f"Next Word Prediction Accuracy: {accuracy:.2f}%")


    def do_next_word_prediction_evaluation(self, sentences):
        # Example usage:
        next_word_samples = self.create_next_word_prediction_samples(sentences, num_samples=50)
        self.evaluate_next_word_prediction(next_word_samples)


    def do_all_evaluations(self, corpus_text):

        # Step 2: Split text into sentences
        sentences = self.split_into_sentences(corpus_text)

        # Cloze Test Evaluationprint
        cloze_samples = self.create_cloze_test_samples(sentences, num_samples=50)
        self.evaluate_cloze_test(cloze_samples)

        # Next Word Prediction Evaluation
        next_word_samples = self.create_next_word_prediction_samples(sentences, num_samples=50)
        self.evaluate_next_word_prediction(next_word_samples)


    def send_prompt_structured_output(self):
        self.logger.info("send_prompt_structured_output")
