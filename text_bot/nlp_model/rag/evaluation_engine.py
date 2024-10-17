import random
import re
from custom_logger.universal_logger import UniversalLogger
from text_bot.nlp_model.replicate_model import ReplicateModel
from text_bot.nlp_model.llm_structured_output_models.llama_masked_word_export import LlamaMaksedWordPrediction
import json
from text_bot.utils import retry
from text_bot.nlp_model.rag.llama_structured_prompt_creator import LlamaStructuredPromptCreator, STRUCTURED_OUTPUT_SYSTEM_PROMPT



class EvaluationEngine:

    def __init__(self):
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)
        self.replicate_model = ReplicateModel()
        self.llama_structured_prompt_creator = LlamaStructuredPromptCreator()


    def create_cloze_test_samples(self, text_chunk, num_masks=3):
        words = text_chunk.split()  # Split the text chunk into words
        words_copy = words[:]  # Make a copy of the original word list
        masked_words = []

        # Randomly select indices to mask
        mask_indices = random.sample(range(len(words_copy)), min(num_masks, len(words_copy)))
        self.logger.info(f"create_cloze_test_samples mask_indices: " + str(mask_indices))

        for mask_idx in mask_indices:
            masked_word = words_copy[mask_idx]
            words_copy[mask_idx] = '[MASK]'  # Replace the word with [MASK]
            masked_words.append(masked_word)

        masked_chunk = ' '.join(words_copy)

        return masked_chunk, masked_words


    def predict_masked_word_v1(self, masked_sentence):
        self.logger.info(f"masked_sentence: " + masked_sentence)

        prompt = self.llama_structured_prompt_creator.get_masking_prompt(masked_sentence)

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

        prompt = self.llama_structured_prompt_creator.get_masking_prompt(masked_sentence)

        self.logger.info(f"predict_masked_word prompt: " + str(prompt))

        output_json = self.get_prediction_json(prompt)
        return output_json


    @retry(max_retries=3, initial_delay=1, backoff=2, exceptions=(Exception, json.decoder.JSONDecodeError))
    def get_prediction_json(self, prompt):
        # Generate prediction using the model
        output = self.replicate_model.predict_structured_output(
                                      user_prompt= prompt,
                                      structured_output_model = LlamaMaksedWordPrediction)

        self.logger.info(f"predict_masked_word output: " + str(output))

        # Check if the output is not None or empty
        if not output or output.strip() == "":
            self.logger.error("The model output is empty or invalid.")
            raise ValueError("The model output is empty or invalid.")  # Raise an error to retry

        output_json = None
        try:
            output_json = json.loads(output)
        except json.decoder.JSONDecodeError as e:
            self.logger.error(f"JSON decoding failed: {e}")

        if not output_json:
            try:
                output_json = self.load_fixed_json(output)
            except json.decoder.JSONDecodeError as e:
                self.logger.error(f"JSON decoding failed: {e}")
                raise  # This will trigger the retry

        return output_json

    def get_json_output(self, json_string):
        json_output = None
        try:
            # Try loading the raw JSON
            json_output = json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

        return json_output

    def get_substring_before_last_occurrence(self, whole_string, sub):
        index = whole_string.rfind(sub)
        if index != -1:
            return whole_string[:index]
        else:
            return whole_string

    def load_fixed_json(self, json_string):

        json_output = self.get_json_output(json_string)
        if json_output:
            return json_output

        json_string = json_string.strip()
        last_char = json_string[-1]

        if last_char == '}':
            json_string = json_string + ']'

        elif last_char == '"':
            json_string = json_string + ']}]'

        elif json_string.endswith(']') and not json_string.endswith(']}]'):
            json_string = json_string + '}]'

        elif json_string.endswith('",'):
            json_string = json_string[:-1] + ']}]'

        elif json_string.endswith('},'):
            json_string = json_string[:-1] + ']'

        elif json_string.endswith(',{"'):
            json_string = json_string[:-3] + ']'

        elif json_string.endswith('{"'):
            json_string = json_string[:-2] + ']'

        elif json_string.endswith(',{'):
            json_string = json_string[:-2] + ']'

        else:
            json_string_new = self.get_substring_before_last_occurrence(json_string, ',"')
            if json_string_new == json_string:
                json_string = self.get_substring_before_last_occurrence(json_string, '{"')
            else:
                json_string = json_string_new

        json_output = self.get_json_output(json_string)
        if json_output:
            return json_output



    def load_fixed_json_v1(self, json_string):
        try:
            # Try loading the raw JSON
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

            # First, ensure the string ends with proper closing braces/brackets
            json_string = json_string.strip()
            if not json_string.endswith(']'):
                json_string = json_string.rstrip(',') + ']'
            if not json_string.endswith('}]'):
                json_string = json_string.rstrip(',') + '}]'

            # Find the last dictionary in the JSON string
            last_open_bracket = json_string.rfind('{')
            last_close_bracket = json_string.rfind('}')

            # If we have a valid start of a dictionary
            if last_open_bracket != -1 and last_close_bracket != -1 and last_close_bracket > last_open_bracket:
                last_dict_str = json_string[last_open_bracket:last_close_bracket + 1]
                try:
                    # Try to parse the last dictionary to check its integrity
                    last_dict = json.loads(last_dict_str)

                    # Check if "word" is complete and valid
                    if "word" in last_dict and isinstance(last_dict["word"], str):
                        last_word = last_dict["word"].strip()

                        # If the last word is incomplete (e.g., ends abruptly)
                        if last_word.endswith(',') or not last_word[-1].isalpha():
                            print("The last 'word' is incomplete, removing the last dictionary.")
                            json_string = json_string[:last_open_bracket] + ']'
                except json.JSONDecodeError:
                    print("Failed to parse the last dictionary, removing it.")
                    json_string = json_string[:last_open_bracket] + ']'
            else:
                print("Malformed JSON, removing the last entry.")

            try:
                # Try loading the fixed JSON string
                return json.loads(json_string)
            except json.JSONDecodeError as e:
                print(f"Still unable to decode JSON: {e}")
                raise


    def evaluate_cloze_test(self, masked_words, predicted_words_list):

        predicted_candidates_list = [predicted_word["words_list"] for predicted_word in predicted_words_list]

        self.logger.info("evaluate_cloze_test predicted_candidates_list: "+str(predicted_candidates_list))
        self.logger.info("evaluate_cloze_test masked_words: " + str(masked_words))

        correct = 0
        total = len(masked_words)
        masked_predicted = dict()
        for idx, masked_word in enumerate(masked_words):
            predicted_top_candidates_lower_list = list()
            if idx < len(predicted_candidates_list):
                predicted_top_candidates_lower_list = [predicted_candidate.lower()
                                                       for predicted_candidate in predicted_candidates_list[idx]]
                if masked_word.lower() in predicted_top_candidates_lower_list:
                    correct += 1
            masked_predicted[masked_word] = predicted_top_candidates_lower_list
        accuracy = correct / total * 100
        self.logger.info(f"Cloze Test Accuracy: {accuracy:.2f}%")
        return correct, total, masked_predicted



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

        self.logger.info(f"predict_masked_word prompt: " + str(prompt))

        # Generate prediction using the model
        output = self.replicate_model.predict_structured_output(
                                      user_prompt= prompt,
                                      structured_output_model = LlamaMaksedWordPrediction)

        self.logger.info(f"predict_masked_word output: " + str(output))

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
