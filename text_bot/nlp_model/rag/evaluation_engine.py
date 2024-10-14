import random
import re
from custom_logger.universal_logger import UniversalLogger
from text_bot.nlp_model.replicate_model import ReplicateModel


class EvaluationEngine:

    def __init__(self):
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)
        self.replicate_model = ReplicateModel()

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
                words[mask_idx] = '____________________'
                masked_sentence = ' '.join(words)
                samples.append((masked_sentence, masked_word))
        return samples


    def predict_masked_word_v1(self, masked_sentence):
        self.logger.info(f"masked_sentence: " + masked_sentence)
        # Prepare the prompt for Llama 3.1
        prompt = f"Fill in the blank with a single word in Romani language: {masked_sentence}"

        # Generate prediction using the model
        output = self.replicate_model.predict(prompt=prompt)

        self.logger.info(f"predict_masked_word output: " + str(output))

        # Extract the predicted word from the model's output
        predicted_word = output.strip().split()[0]
        return predicted_word


    def predict_masked_word(self, masked_sentence):
        self.logger.info(f"masked_sentence: " + masked_sentence)
        # Prepare the prompt for Llama 3.1
        prompt = f"Fill in the blank with a single word in Romani language:  {masked_sentence}"

        # Generate prediction using the model
        output = self.replicate_model.predict(prompt=prompt)

        self.logger.info(f"predict_masked_word output: " + str(output))

        # Handle the case where output is a list
        if isinstance(output, list):
            output_text = ''.join(output)
        elif isinstance(output, str):
            output_text = output
        else:
            raise TypeError(f"Unexpected type for output: {type(output)}")

        predicted_word = ""
        if output_text and output_text.strip().split():
            # Extract the predicted word from the model's output
            predicted_word = output_text.strip().split()[0]
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
        return correct, total


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
        output = self.replicate_model.predict(prompt=prompt)

        # Handle the case where output is a list
        if isinstance(output, list):
            output_text = ''.join(output)
        elif isinstance(output, str):
            output_text = output
        else:
            raise TypeError(f"Unexpected type for output: {type(output)}")

        predicted_word = ""
        if output_text and output_text.strip().split():
            # Extract the predicted word from the model's output
            predicted_word = output_text.strip().split()[0]

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
        return correct, total


    def do_next_word_prediction_evaluation(self, sentences):
        # Example usage:
        next_word_samples = self.create_next_word_prediction_samples(sentences, num_samples=50)
        self.evaluate_next_word_prediction(next_word_samples)


    def do_all_evaluations(self, corpus_text):
        # Split text into sentences
        sentences = self.split_into_sentences(corpus_text)

        # Cloze Test Evaluation
        cloze_samples = self.create_cloze_test_samples(sentences, num_samples=50)
        cloze_correct, cloze_total = self.evaluate_cloze_test(cloze_samples)

        # Next Word Prediction Evaluation
        next_word_samples = self.create_next_word_prediction_samples(sentences, num_samples=50)
        next_word_correct, next_word_total = self.evaluate_next_word_prediction(next_word_samples)

        # Return the results
        return {
            'cloze_correct': cloze_correct,
            'cloze_total': cloze_total,
            'next_word_correct': next_word_correct,
            'next_word_total': next_word_total
        }