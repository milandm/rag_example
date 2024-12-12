import sys
from re import match

sys.path.append("..")

from text_bot.nlp_model.nlp_model import NlpModel
from text_bot.utils import load_documents, save_json_to_file, load_json_file, csv_to_json

from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter


from text_bot.nlp_model.entity_linking.prompt_creator import PromptCreator
from text_bot.utils import (load_and_ocr_documents_with_filename,
                            load_document_paths,
                            load_pdf_pages_to_files,
                            load_csv_file)
from text_bot.nlp_model.entity_linking.data_mapping import (extract_dnb_fields,
                                                            extract_dj_acuris_fields,
                                                            find_dnb_match_in_dj_acuris,
                                                            extract_dnb_and_dj_acuris_lists,
                                                            compare_individuals,
                                                            compare_dnb_person_to_dj)

from custom_logger.universal_logger import UniversalLogger
import json

import pandas as pd
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

from text_bot.nlp_model.entity_linking.autogen_agent_perplexity import AutogenAgentPerplexity
from text_bot.nlp_model.entity_linking.autogen_agent_you_com import AutogenAgentYouCom



# SENTENCE_MIN_LENGTH = 15
SENTENCE_MIN_LENGTH = 2
MAX_CHUNK_SIZE = 500
MAX_CHUNK_OVERLAP_SIZE = 250
MAX_SEMANTIC_CHUNK_SIZE = 1000
MAX_SEMANTIC_CHUNK_OVERLAP_SIZE = 500
MAX_PAGE_SIZE = 5500

HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]

class VectorizeDocumentsEngine:


    def __init__(self, nlp_model :NlpModel):
        self.model = nlp_model
        self.prompt_creator = PromptCreator(nlp_model)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_CHUNK_SIZE, chunk_overlap=MAX_CHUNK_OVERLAP_SIZE)
        self.recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_SEMANTIC_CHUNK_SIZE, chunk_overlap=MAX_SEMANTIC_CHUNK_OVERLAP_SIZE)
        self.pages_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_PAGE_SIZE, chunk_overlap=0)
        self.markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)

        self.autogen_agent_perplexity = AutogenAgentPerplexity(nlp_model)
        self.autogen_agent_you_com = AutogenAgentYouCom(nlp_model)



    def load_documents(self):
        self.logger.info("load_documents")
        self.load_csv_file()


    def load_csv_file(self):
        # self.autogen_agent.run_agent()
        self.autogen_agent_perplexity.run_group_agent()
        # self.autogen_agent_you_com.run_group_agent()


    def load_csv_file2(self):
        csv_prepared_json_list = csv_to_json('csv_data/full_join_dj_10k.csv', 10)
        # self.logger.info(json.dumps(csv_prepared_json_list, indent=2))
        dnb_individuals, dj_individuals = extract_dnb_and_dj_acuris_lists(csv_prepared_json_list)
        # self.logger.info("dnb_individuals: "+str(dnb_individuals)+" dj_individuals: "+ str(dj_individuals))
        matching_list = compare_dnb_person_to_dj(dnb_individuals[0], dj_individuals)
        self.logger.info("matching_list: "+str(matching_list))
        perplexity_response = self.prompt_creator.compare_persons(str(dnb_individuals[0]),matching_list)
        self.logger.info("perplexity_response compare_persons: " + str(perplexity_response))

        perplexity_response = self.prompt_creator.search_more_individuals(dnb_individuals[0])
        self.logger.info("perplexity_response search_more_individuals: " + str(perplexity_response))




    def load_csv_file1(self):
        csv_file_path = 'csv_data/full_join_dj_10k.csv'
        dnb_dj_acuris_df = load_csv_file(csv_file_path, delimiter=',')

        # Get the first 10 rows
        dnb_dj_acuris_df = dnb_dj_acuris_df.head(20)

        # self.check_dnb_dj_acuris_df()

        dnb_data_list, dj_acuris_data_list = self.extract_relevant_info(dnb_dj_acuris_df)
        self.logger.info("csv to list, dnb_data_list: "+str(dnb_data_list))
        self.logger.info("csv to list, dj_acuris_data_list: " + str(dj_acuris_data_list))

        self.logger.info("compared_data dnb_data_list[0]: " + str(dnb_data_list[0]))
        self.logger.info("compared_data dj_acuris_data_list: " + str(dj_acuris_data_list))

        matching_list = find_dnb_match_in_dj_acuris(dnb_data_list[0], dj_acuris_data_list)
        self.logger.info("matching_list: " + str(matching_list))
        # perplexity_response = self.prompt_creator.get_persons_list(str(dnb_data_list[0]))

        # perplexity_response = self.prompt_creator.compare_persons(str(dnb_data_list[0]),matching_list)
        # self.logger.info("perplexity_response: " + str(perplexity_response))




    def check_dnb_dj_acuris_df(self, dnb_dj_acuris_df):
        self.logger.info(dnb_dj_acuris_df[['duns', 'duns-2']].isna().all())
        self.logger.info(dnb_dj_acuris_df[['peid', 'peid-2']].isna().all())

        expected_dnb_columns = ['duns', 'duns-2', 'given_name', 'family_name', 'birth_date']
        expected_dj_columns = ['peid', 'peid-2', 'matched_name', 'description_json', 'is_pep']

        missing_dnb_columns = [col for col in expected_dnb_columns if col not in dnb_dj_acuris_df.columns]
        missing_dj_columns = [col for col in expected_dj_columns if col not in dnb_dj_acuris_df.columns]

        self.logger.info(f"Missing DnB columns: {missing_dnb_columns}")
        self.logger.info(f"Missing DJ columns: {missing_dj_columns}")

        self.logger.info(dnb_dj_acuris_df.head())
        self.logger.info(dnb_dj_acuris_df.columns)
        self.logger.info(f"Number of rows in DataFrame: {len(dnb_dj_acuris_df)}")



    def extract_relevant_info(self, dnb_dj_acuris_df):

        dnb_data_list = list()
        dj_acuris_data_list = list()


        for index, row in dnb_dj_acuris_df.iterrows():
            self.logger.info(f"Processing row {index}")

            is_dnb = any(
                pd.notna(row.get(col)) for col in ['duns', 'duns-2', 'business_entity_type', 'registration_numbers'])
            is_dj = any(pd.notna(row.get(col)) for col in ['peid', 'peid-2', 'description_json', 'description_xml'])

            self.logger.info(f"Processing row {index}")
            # Identification logic
            if is_dnb:
                self.logger.info(f"Row {index} identified as DnB data.")
                dnb_data = extract_dnb_fields(row)
                self.logger.info(f"dnb_data: {dnb_data}")
                dnb_data_list.append(dnb_data)
            if is_dj:
                self.logger.info(f"Row {index} identified as DJ/Acuris data.")
                dj_data = extract_dj_acuris_fields(row)
                self.logger.info(f"dj_data: {dj_data}")
                dj_acuris_data_list.append(dj_data)

            if not is_dnb and is_dj:
                self.logger.info(f"Row {index} could not be identified as DnB or DJ data.")

        return dnb_data_list, dj_acuris_data_list




