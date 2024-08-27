import sys

sys.path.append("..")

import json

from text_bot.nlp_model.nlp_model import NlpModel
from text_bot.nlp_model.mml_model import MmlModel
from text_bot.utils import remove_quotes, extract_single_value_openai_content, extract_clean_json_data

# SENTENCE_MIN_LENGTH = 15
SENTENCE_MIN_LENGTH = 2

from text_bot.nlp_model.rag.prompt_template_creator import \
    PromptTemplateCreator, \
    SYSTEM_MSG_TITLE, \
    TITLE_EXTRACT_KEY, \
    DOCUMENT_SYSTEM_MSG_COMPRESSION_V3, \
    DOCUMENT_COMPRESSION_EXTRACT_KEY, \
    DOCUMENT_SYSTEM_MSG_COMPRESSION_CHECK_V1, \
    DOCUMENT_SYSTEM_MSG_SEMANTIC_TEXT_CHUNKING_V1, \
    DOCUMENT_SYSTEM_MSG_QUESTION_STATEMENT_V1, \
    DOCUMENT_SYSTEM_MSG_QUESTION_RELATED_INFORMATION_V1, \
    IMAGE_CREATOR_SYSTEM_MSG_V1

from custom_logger.universal_logger import UniversalLogger
from pydantic import BaseModel


class PromptCreator:

    def __init__(self, nlp_model: NlpModel, mml_model: MmlModel):
        self.model = nlp_model
        self.mml_model = mml_model
        self.prompt_template_creator = PromptTemplateCreator()
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)


    def get_document_title(self, first_documents_split_txt: str):
        title_extract_prompt = self.prompt_template_creator.get_title_extract_prompt(first_documents_split_txt)
        document_title_openai_response = self.model.send_prompt(SYSTEM_MSG_TITLE, title_extract_prompt)
        document_title_content = document_title_openai_response.choices[0].message.content
        document_title = extract_single_value_openai_content(document_title_content, TITLE_EXTRACT_KEY)
        return document_title

    def get_query_based_text_compression(self, query, documents_split_txt: str):
        text_compression_prompt = self.prompt_template_creator.get_document_text_compression_prompt(documents_split_txt)
        text_compression_openai_response = self.model.send_prompt(DOCUMENT_SYSTEM_MSG_COMPRESSION_V3, text_compression_prompt)
        print(str(text_compression_openai_response))
        text_compression_content = text_compression_openai_response.choices[0].message.content
        text_compression = extract_single_value_openai_content(text_compression_content, DOCUMENT_COMPRESSION_EXTRACT_KEY)
        text_compression = remove_quotes(text_compression)
        return text_compression

    def get_document_text_compression(self, documents_split_txt: str):
        documents_split_txt = self.clean_documents_split(documents_split_txt)
        text_compression_prompt = self.prompt_template_creator.get_document_text_compression_prompt(documents_split_txt)
        text_compression_openai_response = self.model.send_prompt(DOCUMENT_SYSTEM_MSG_COMPRESSION_V3, text_compression_prompt)
        print(str(text_compression_openai_response))
        text_compression_content = text_compression_openai_response.choices[0].message.content
        text_compression = extract_single_value_openai_content(text_compression_content, DOCUMENT_COMPRESSION_EXTRACT_KEY)
        text_compression = remove_quotes(text_compression)
        return text_compression

    def get_three_question_statements(self, question: str):
        three_question_statements_prompt = self.prompt_template_creator.get_three_question_statements(question)
        three_question_statements_openai_response = self.model.send_prompt(DOCUMENT_SYSTEM_MSG_QUESTION_STATEMENT_V1, three_question_statements_prompt)
        print(str(three_question_statements_openai_response))
        three_question_statements_content = three_question_statements_openai_response.choices[0].message.content
        three_question_statements_list = extract_clean_json_data(three_question_statements_content)
        return three_question_statements_list


    def get_question_related_informations(self, psychological_state: str, section_text):
        question_related_information_prompt = self.prompt_template_creator.get_question_related_information(psychological_state, section_text)
        print("get_question_related_informations question_related_information_prompt: " + question_related_information_prompt)
        question_related_information_openai_response = \
            self.model.send_prompt(DOCUMENT_SYSTEM_MSG_QUESTION_RELATED_INFORMATION_V1, question_related_information_prompt)
        print(str(question_related_information_openai_response))
        question_related_information_content = question_related_information_openai_response.choices[0].message.content
        return question_related_information_content


    def get_question_related_informations_structured(self, psychological_state: str, section_text, structured_output_model: BaseModel):
        question_related_information_prompt = self.prompt_template_creator.get_question_related_information(
            psychological_state, section_text)
        self.logger.info(
            "get_question_related_informations question_related_information_prompt: " + question_related_information_prompt)
        question_related_information_openai_response = \
            self.model.send_prompt_structured_output(DOCUMENT_SYSTEM_MSG_QUESTION_RELATED_INFORMATION_V1,
                                   question_related_information_prompt, structured_output_model)

        question_related_information_content = question_related_information_openai_response.choices[
            0].message.content
        return question_related_information_content



    def clean_documents_split(self, documents_split_txt):
        documents_split_txt = documents_split_txt.replace("page_content=", "")
        return documents_split_txt

    def clean_openai_response_content(self, response_content):
        response_content_txt = response_content.replace("```", "")
        return response_content_txt

    def get_document_text_compression_check(self, documents_split_txt: str, previous_response: str):
        documents_split_txt = self.clean_documents_split(documents_split_txt)
        text_compression_check_prompt = self.prompt_template_creator.get_document_text_compression_check_prompt(documents_split_txt, previous_response)
        text_compression_check_openai_response = self.model.send_prompt(DOCUMENT_SYSTEM_MSG_COMPRESSION_CHECK_V1, text_compression_check_prompt)
        print(str(text_compression_check_openai_response))
        text_compression_check_content = text_compression_check_openai_response.choices[0].message.content

        text_compression_check_content_txt = self.clean_openai_response_content(text_compression_check_content)
        text_compression_check = text_compression_check_content_txt
        try:
            text_compression_check_content_json = json.loads(text_compression_check_content_txt)
            text_compression_check = text_compression_check_content_json.get("new_response")
        except Exception as e:
            print(e)
        text_compression_check = remove_quotes(text_compression_check)
        return text_compression_check

    def get_document_semantic_text_chunks(self, documents_split_txt: str, last_previous_semantic_chunk: str):
        documents_split_txt = self.clean_documents_split(documents_split_txt)
        semantic_text_chunks_prompt = self.prompt_template_creator.get_document_semantic_text_chunks_prompt(
            documents_split_txt, last_previous_semantic_chunk)
        semantic_text_chunk_openai_response = self.model.send_prompt(DOCUMENT_SYSTEM_MSG_SEMANTIC_TEXT_CHUNKING_V1,
                                                                      semantic_text_chunks_prompt)
        print(str(semantic_text_chunk_openai_response))
        semantic_text_chunks_content = semantic_text_chunk_openai_response.choices[0].message.content

        semantic_text_chunks_content_json_list = extract_clean_json_data(semantic_text_chunks_content)
        return semantic_text_chunks_content_json_list



    def get_image_description(self, quote_for_image: str):
        semantic_text_chunks_prompt = self.prompt_template_creator.get_image_description(quote_for_image)
        semantic_text_chunk_openai_response = self.model.send_prompt(DOCUMENT_SYSTEM_MSG_QUESTION_RELATED_INFORMATION_V1,
                                                                      semantic_text_chunks_prompt)
        print(str(semantic_text_chunk_openai_response))
        semantic_text_chunks_content = semantic_text_chunk_openai_response.choices[0].message.content
        return semantic_text_chunks_content



    def get_image_for_quote(self, quote_for_image: str):
        quote_for_image_prompt = self.prompt_template_creator.get_image_for_quote(quote_for_image)
        quote_for_image_openai_response = self.mml_model.generate_image(quote_for_image_prompt)
        print(str(quote_for_image_openai_response))
        image_url = quote_for_image_openai_response.data[0].url
        return image_url


    def get_image_based_on_description(self, image_description: str):
        quote_for_image_prompt = self.prompt_template_creator.get_image_based_on_description(image_description)
        quote_for_image_openai_response = self.mml_model.generate_image(quote_for_image_prompt)
        print(str(quote_for_image_openai_response))
        image_url = quote_for_image_openai_response.data[0].url
        return image_url