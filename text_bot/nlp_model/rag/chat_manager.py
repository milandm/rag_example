import sys

sys.path.append("..")

import json

from text_bot.nlp_model.nlp_model import NlpModel
from text_bot.ai_utils import token_count_from_string

import re


# SENTENCE_MIN_LENGTH = 15
SENTENCE_MIN_LENGTH = 2

from text_bot.views.models import (CTDocumentSection,
                                   CTDocumentSubsection,
                                   CTDocumentSectionText,
                                   CTDocumentSubsectionText,
                                   QuotesDocuments)

from text_bot.nlp_model.rag.prompt_creator import PromptCreator

MAX_TOKEN_CHUNK_SIZE = 2000
MAX_CHUNK_SIZE = 1000
MAX_CHUNK_OVERLAP_SIZE = 500
MAX_PAGE_SIZE = 5500

class ChatManager:

    def __init__(self, nlp_model :NlpModel):
        self.model = nlp_model
        self.prompt_creator = PromptCreator(nlp_model)

    # def send_user_query(self, current_query: str, history_key:str = "") -> dict:
    #     print(" ")
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
    #     print("current_query "+current_query)
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
    #     print(" ")
    #     # get_chat_history = self.get_chat_history(history_key)
    #     query_embedding = self.model.get_embedding(current_query)
    #     documents = CTDocumentSplit.objects.query_embedding_by_distance(query_embedding)
    #     documents_list = list(documents)
    #     doc_for_prompt = get_mmr_cosine_sorted_docs(query_embedding, documents)
    #
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
    #     print("not ranked ")
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
    #     print(" ")
    #     for doc in documents:
    #         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
    #         print(doc.split_text)
    #         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
    #
    #     print(" ")
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
    #     print("ranked ")
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
    #     print(" ")
    #     for doc in doc_for_prompt:
    #         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
    #         print(doc.split_text)
    #         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
    #     # self.prompt_creator.get_answer(query_embedding, doc_for_prompt)


    def send_user_query(self, current_query: str) -> dict:
        print(" ")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
        print("current_query "+current_query)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
        print(" ")

        three_question_statements_list = self.prompt_creator.get_three_question_statements(current_query)

        embedded_three_question_statements_list = self.model.get_embeddings(three_question_statements_list)

        sections_dict = dict()
        for question_statement_embedded in embedded_three_question_statements_list:
            quotes_documents = QuotesDocuments.objects.query_embedding_in_db(question_statement_embedded)

            for quotes_document in quotes_documents:
                sections_dict[quotes_document.id] = quotes_document.section_text_value

        sections_list = list()
        for key, section_text in sections_dict.items():
            print("sections_dict section_text: "+section_text)
            sections_list.append(section_text)

        concatenated_section_list =  self.concatenate_prompt_input_list(sections_list)

        question_related_info_list = list()
        for section_text in concatenated_section_list[:1]:
            print("concatenated_section_list section_text: " + section_text)
            question_related_info = self.prompt_creator.get_question_related_informations(current_query, section_text)
            question_related_info_list.append(question_related_info)

        # json_data = json.dumps(question_related_info_list)
        return question_related_info_list
        # documents_list = list(documents)
        # doc_for_prompt = get_mmr_cosine_sorted_docs(query_embedding, documents)


    def format_answer(self, json_data: str) -> str:
        print("json_first_answer: " + str(json_data))
        json_first_element = None
        if json_data and isinstance(json_data, list):
            json_first_element = json_data[0]
        print("json_first_element: " + str(json_first_element))
        if json_first_element and isinstance(json_first_element, str):
            json_data = json.loads(self.extract_inner_list(json_first_element))
        print("extract_inner_list: " + str(json_data))
        formated_answer = ""
        try:
            for quote_dicts in json_data:
                # if quote_dicts and isinstance(quote_dicts, str):
                #     quote_dicts = json.loads(quote_dicts)
                print("json_first_answer: " + str(quote_dicts))
                for quote_dict in quote_dicts:
                    if quote_dict and not isinstance(quote_dict, dict):
                        quote_dict = json.loads(quote_dict)
                    for quote, author in quote_dict.items():
                        formated_answer=formated_answer+quote+"\n"
                        formated_answer = formated_answer + author + "\n"
        except Exception as e:
            print(str(e))
        if not formated_answer:
            formated_answer = str(json_data)
        return formated_answer

    def extract_inner_list(self, json_data):
        # Find the first occurrence of '[' and the last occurrence of ']'
        start_index = json_data.find('[')
        end_index = json_data.rfind(']')

        if start_index == -1 or end_index == -1 or start_index >= end_index:
            print("No valid list found in the string.")
            return None

        # Extract the substring between the found indices
        inner_list_str = json_data[start_index:end_index + 1]

        inner_start_index = inner_list_str.find('[')
        inner_end_index = inner_list_str.rfind(']')

        if inner_start_index == -1 or inner_end_index == -1 or inner_start_index >= inner_end_index:
            print("No valid list found in the string.")
            return inner_list_str
        else:
            inner_list_str = inner_list_str[inner_start_index:inner_end_index + 1]
            return inner_list_str


    def concatenate_prompt_input_list(self, prompt_input_list):
        new_prompt_input_list = list()
        prompt_input_concatenated = ""
        for prompt_input in prompt_input_list:
            new_prompt_input_concatenated = prompt_input_concatenated+" "+prompt_input
            tokens_count = token_count_from_string(new_prompt_input_concatenated)
            if tokens_count < MAX_TOKEN_CHUNK_SIZE:
                prompt_input_concatenated = new_prompt_input_concatenated
            else:
                new_prompt_input_list.append(prompt_input_concatenated)
                prompt_input_concatenated = prompt_input
        new_prompt_input_list.append(prompt_input_concatenated)
        return new_prompt_input_list

    def get_text_compression(self, documents_split_txt):
        text_split_compression = self.prompt_creator.get_document_text_compression(documents_split_txt)
        text_split_compression_check = self.prompt_creator.get_document_text_compression_check(documents_split_txt, text_split_compression)

        if text_split_compression_check and "YES" in text_split_compression_check:
            return text_split_compression
        else:
            return text_split_compression_check


    def get_chat_history(self, history_key: str) -> dict:
        pass


    def get_user_history(self) -> dict:
        pass