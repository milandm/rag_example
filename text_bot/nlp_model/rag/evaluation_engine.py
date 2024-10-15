import random
import re
from custom_logger.universal_logger import UniversalLogger
from text_bot.nlp_model.replicate_model import ReplicateModel
from text_bot.nlp_model.llm_structured_output_models.llama_masked_word_export import LlamaMaksedWordPrediction
import json
from text_bot.utils import retry

class EvaluationEngine:

    def __init__(self):
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)
        self.replicate_model = ReplicateModel()

    def create_cloze_test_samples(self, text_chunk, num_masks=4):
        words = text_chunk.split()  # Split the text chunk into words
        words_copy = words[:]  # Make a copy of the original word list
        masked_words = []

        # Randomly select indices to mask
        mask_indices = random.sample(range(len(words_copy)), min(num_masks, len(words_copy)))

        for mask_idx in mask_indices:
            masked_word = words_copy[mask_idx]
            words_copy[mask_idx] = '[MASK]'  # Replace the word with [MASK]
            masked_words.append(masked_word)

        masked_chunk = ' '.join(words_copy)

        return masked_chunk, masked_words


    def predict_masked_word_v1(self, masked_sentence):
        self.logger.info(f"masked_sentence: " + masked_sentence)
        # Prepare the prompt for Llama 3.1
        prompt = f"""
        Please create export as json format list containing words in Romani language
        that should replace [MASK] words:  {masked_sentence}"""
        # prompt = f"Return just words in Romani language that should be logical replacement for [MASK] in given context: {masked_sentence}"

        # Generate prediction using the model
        output = self.replicate_model.predict_structured_output(
                                      user_prompt= prompt,
                                      structured_output_model = LlamaMaksedWordPrediction)

        self.logger.info(f"predict_masked_word output: " + str(output))

        # Extract the predicted word from the model's output
        predicted_word = output.strip().split()[0]
        return predicted_word


    def predict_masked_words(self, masked_sentence):
        self.logger.info(f"masked_sentence: " + masked_sentence)
        # Prepare the prompt for Llama 3.1
        prompt = f"""
        Please create export as json format list containing words in Romani language
        that should replace [MASK] words:  {masked_sentence}"""
        # prompt = f"Return just words in Romani language that should be logical replacement for [MASK] in given context:  {masked_sentence}"

        self.logger.info(f"predict_masked_word prompt: " + str(prompt))

        # # Generate prediction using the model
        # output = self.replicate_model.predict_structured_output(
        #                               user_prompt= prompt,
        #                               structured_output_model = LlamaMaksedWordPrediction)
        #
        # self.logger.info(f"predict_masked_word output: " + str(output))

        # # Handle the case where output is a list
        # if isinstance(output, list):
        #     output_text = ''.join(output)
        # elif isinstance(output, str):
        #     output_text = output
        # else:
        #     raise TypeError(f"Unexpected type for output: {type(output)}")

        # predicted_word = ""
        # if output_text and output_text.strip().split():
        #     # Extract the predicted word from the model's output
        #     predicted_word = output_text.strip().split()[0]

        output_json = self.get_prediction_json(prompt)
        return output_json


    @retry(max_retries=3, initial_delay=1, backoff=2)
    def get_prediction_json(self, prompt):
        # Generate prediction using the model
        output = self.replicate_model.predict_structured_output(
                                      user_prompt= prompt,
                                      structured_output_model = LlamaMaksedWordPrediction)

        self.logger.info(f"predict_masked_word output: " + str(output))
        output_json = json.loads(output)
        return output_json


    def evaluate_cloze_test(self, masked_words, predicted_words):
        correct = 0
        total = len(masked_words)
        for idx, masked_word in enumerate(masked_words):
            predicted_word = predicted_words[idx]
            if masked_word.lower() == predicted_word.lower():
                correct += 1
        accuracy = correct / total * 100
        self.logger.info(f"Cloze Test Accuracy: {accuracy:.2f}%")
        return correct, total



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
        # output = self.replicate_model.predict(prompt=prompt)

        # # Handle the case where output is a list
        # if isinstance(output, list):
        #     output_text = ''.join(output)
        # elif isinstance(output, str):
        #     output_text = output
        # else:
        #     raise TypeError(f"Unexpected type for output: {type(output)}")
        #
        # predicted_word = ""
        # if output_text and output_text.strip().split():
        #     # Extract the predicted word from the model's output
        #     predicted_word = output_text.strip().split()[0]

        self.logger.info(f"predict_masked_word prompt: " + str(prompt))

        # Generate prediction using the model
        output = self.replicate_model.predict_structured_output(
                                      user_prompt= prompt,
                                      structured_output_model = LlamaMaksedWordPrediction)

        self.logger.info(f"predict_masked_word output: " + str(output))

        # # Handle the case where output is a list
        # if isinstance(output, list):
        #     output_text = ''.join(output)
        # elif isinstance(output, str):
        #     output_text = output
        # else:
        #     raise TypeError(f"Unexpected type for output: {type(output)}")

        # predicted_word = ""
        # if output_text and output_text.strip().split():
        #     # Extract the predicted word from the model's output
        #     predicted_word = output_text.strip().split()[0]

        output_json = json.loads(output)

        return output_json


    def evaluate_next_word_prediction(self, samples):
        correct = 0
        total = len(samples)
        for prompt, actual_next_word in samples:
            predicted_word = self.predict_next_word(prompt)
            if predicted_word.lower() == actual_next_word.lower():
                correct += 1
        accuracy = correct / total * 100
        self.logger.info(f"Next Word Prediction Accuracy: {accuracy:.2f}%")
        return correct, total


    def do_next_word_prediction_evaluation(self, sentences):
        # Example usage:
        next_word_samples = self.create_next_word_prediction_samples(sentences, num_samples=50)
        self.evaluate_next_word_prediction(next_word_samples)
