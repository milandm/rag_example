import sys

sys.path.append("..")

from text_bot.nlp_model import NlpModel
from text_bot.nlp_model import PromptTemplateCreator
from text_bot.ai_utils import is_close


BOOK_FILENAME = "Marcus_Aurelius_Antoninus_-_His_Meditations_concerning_himselfe"

SENTENCE_MIN_LENGTH = 2



class SearchService:


    def __init__(self, collection_name :str, nlp_model :NlpModel):
        self.model = nlp_model
        self.qdrant_client = QdrantDbClient(collection_name=collection_name, vector_params_size = self.model.VECTOR_PARAMS_SIZE)
        self.prompt_template_creator = PromptTemplateCreator()


    def search(self, question: str) -> dict:
        question_embedding = self.model.get_embedding(question)
        similar_docs = self.qdrant_client.search_sentences(encoded_question = question_embedding)
        if not is_close(similar_docs[0].score, 1, 0.01):
            payloads=[
                {
                    "data_type": "question",
                    "question": question
                }
            ]
            vectors=[question_embedding]
            self.qdrant_client.upsert_sentences(payloads, vectors)

        similar_docs = self.qdrant_client.search_filtered_sentences(query_vector = question_embedding,
                                                                    query_filter_key = "data_type",
                                                                    query_filter_value = "answer")

        print(similar_docs)

        prompt, references = self.prompt_template_creator.create_similar_sentences_prompt(question, similar_docs)
        response = self.model.send_prompt(prompt)

        return {
            "response": response["choices"][0]["message"]["content"],
            "references": references,
        }
