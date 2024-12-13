import os
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
from text_bot.nlp_model.nlp_model import NlpModel
import autogen
from autogen import ConversableAgent, UserProxyAgent
from autogen import register_function
from typing import Annotated, Literal
from text_bot.nlp_model.openai_model import OpenaiModel
from autogen import GroupChatManager
from autogen import GroupChat


# from autogen_agentchat.agents import CodingAssistantAgent, ToolUseAssistantAgent
# from autogen_agentchat.task import TextMentionTermination
# from autogen_agentchat.teams import RoundRobinGroupChat
# from autogen_core.components.tools import FunctionTool
# from autogen_ext.models import OpenAIChatCompletionClient


from typing_extensions import Annotated

from text_bot.nlp_model.perplexity_api import PerplexityApi
from text_bot.nlp_model.you_com_api import YouComApi


config_list = [{"model": "gpt-4-turbo-preview", "api_key": os.getenv("OPENAI_API_KEY")}]
llm_config = {
    "temperature": 0,
    "config_list": config_list,
}

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


# @staticmethod
# def print_agent(user):
#     print("user: " + user)

class AutogenAgentPerplexity:



    def __init__(self, nlp_model :NlpModel):
        self.model = nlp_model
        self.prompt_creator = PromptCreator(nlp_model)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_CHUNK_SIZE, chunk_overlap=MAX_CHUNK_OVERLAP_SIZE)
        self.recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_SEMANTIC_CHUNK_SIZE, chunk_overlap=MAX_SEMANTIC_CHUNK_OVERLAP_SIZE)
        self.pages_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_PAGE_SIZE, chunk_overlap=0)
        self.markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)


        # create a UserProxyAgent instance named "user_proxy"
        self.user_proxy_feedback = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="ALWAYS",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={
                "use_docker": False
            },
            # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        )


        self.assistant_agent = autogen.AssistantAgent(
            name="ComplianceAssistantAgent",
            llm_config=llm_config,
            system_message="""
            I should check on Perplexity and You.com platform if screened person could be associated 
            with some of given matching persons with high confidence
            """,
        )

        # search_more_individuals_perplexity(dnb_individual: dict):
        # compare_persons_perplexity(dnb_individual: dict, matching_list: List[Dict]):
        # enrich_dnb_data_perplexity(dnb_individual: dict):
        # get_inconsistencies_perplexity(dnb_individual: dict, matching_list: List[Dict]):


        (self.assistant_agent.register_for_llm(name="enrich_dnb_data",
         description = """You should enrich screened person data provided as parameters: (dnb_individual:dict), 
                            on Perplexity platform, with more data I can find on the internet related to that person.""")
         (enrich_dnb_data))

        (self.assistant_agent.register_for_llm(name="compare_persons",
        description = """You should compare individuals personal data provided in parameters: (matching_list: List[Dict]),
                        that could be associated to given person provided in parameters: (dnb_individual:dict) on Perplexity platform""")
         (compare_persons))

        (self.assistant_agent.register_for_llm(name="search_more_individuals",
        description = """You should search internet for more individuals that could be 
                        associated to given person data provided in parameters: (dnb_individual:dict) on Perplexity platform""")
         (search_more_individuals))


        (self.assistant_agent.register_for_llm(name="get_inconsistencies",
        description = """I am looking for discrepancies between screened persons data provided in  parameters: (dnb_individual:dict)
                        and data related to potential matching persons provided in parameters: (matching_list: List[Dict]) on Perplexity platform""")
         (get_inconsistencies))


        # The Number Agent always returns the same numbers.
        self.user_proxy_agent = UserProxyAgent(
            name="ScreenPersonAgent",
            llm_config=False,
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
            human_input_mode="NEVER",
        )

        # Register the tool function with the user proxy agent.
        self.user_proxy_agent.register_for_execution(name="enrich_dnb_data")(enrich_dnb_data)

        # Register the tool function with the user proxy agent.
        self.user_proxy_agent.register_for_execution(name="compare_persons")(compare_persons)

        # Register the tool function with the user proxy agent.
        self.user_proxy_agent.register_for_execution(name="search_more_individuals")(search_more_individuals)


        # Register the tool function with the user proxy agent.
        self.user_proxy_agent.register_for_execution(name="get_inconsistencies")(get_inconsistencies)



        self.json_formatter_agent = autogen.AssistantAgent(
            name="JsonFormatterAgent",
            llm_config=llm_config,
            system_message="""I am a JSON Formatter agent. 
            Your job is to format the responses of other agents into clean, structured JSON.

            Please extract all data related to screened dnb_person from all previous responses. 
            Please format output as json. 

            Input: Raw response text from another agent.
            Output: JSON object with the following structure:            
                {
                    dnb_name: "some name",
                    dnb_sure_name: "some sure name",
                    dnb_sure_nationality: "some nationality",
                    dnb_birthday: "some birthday",
                    dnb_gender: "some gender",
                    dnb_age: "some age",
                    dnb_address: "some address",
                    dnb_companies: ["some previous company", "some previous company",..., "current company"],
                    ...,
                    sources_list:[]
                }

            """,
            description="""This agent formats responses into JSON for consistent structuring.""",
        )



        self.json_formatter_agent_compare = autogen.AssistantAgent(
            name="CompareJsonFormatterAgent",
            llm_config=llm_config,
            system_message="""I am a JSON Formatter agent.
            Your job is to format the responses of other agents into clean, structured JSON.

            From given response, please extract exact values that you based your conclusion
            if dnb_individual is same or different to any other individual from matching list.
            Please format output as json.

            Input: Raw response text from another agent.
            Output: JSON object with the following structure:
                {
                    dnb_name: "some name",
                    matching_person_name: "some name"
                    names_matching: True,
                    dnb_sure_name: "some sure name",
                    matching_person_name: "some sure name",
                    sure_names_matching: True,
                    ...,
                    sources_list:[]
                }

            """,
            description="""This agent formats responses into JSON for consistent structuring.""",
        )

        # allowed_transitions = {
        #     proxy_agent: [IO_Agent],
        #     IO_Agent: [friendly_agent, suspicious_agent],
        #     suspicious_agent: [proxy_agent],
        #     friendly_agent: [proxy_agent],
        # }

        group_chat = GroupChat(
            agents=[self.assistant_agent, self.user_proxy_agent, self.json_formatter_agent],
            messages=[],
            max_round=6,
            # allowed_or_disallowed_speaker_transitions=allowed_transitions,
            speaker_transitions_type="allowed",
        )

        self.group_chat_manager = GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}]},
        )



    def run_group_agent(self):

        csv_prepared_json_list = csv_to_json('csv_data/full_join_dj_10k.csv', 10)
        dnb_individuals, dj_individuals = extract_dnb_and_dj_acuris_lists(csv_prepared_json_list)
        matching_list = compare_dnb_person_to_dj(dnb_individuals[0], dj_individuals)
        dnb_person = dnb_individuals[0]

        # {"+str(dnb_person)+"}"

        main_task = """Please check this parameters: (dnb_individual: {"""+str(dnb_person)+"""})
                    compare this dnb_individual with these individuals parameters: (matching_list: """+str(matching_list)+""")
                    and search internet for any individual that could be possibly associated with
                    given dnb_individual.
                    """

        chat_result = self.user_proxy_agent.initiate_chat(
            self.group_chat_manager,
            message=main_task,
            summary_method="reflection_with_llm",
        )
        self.logger.info("chat_result: "+str(chat_result))




def search_more_individuals(dnb_individual: dict):
    prompt_creator = PromptCreator(PerplexityApi())
    return prompt_creator.search_more_individuals(dnb_individual)


def compare_persons(dnb_individual: dict, matching_list:List[Dict]):
    prompt_creator = PromptCreator(PerplexityApi())
    return prompt_creator.compare_persons(str(dnb_individual),matching_list)


def enrich_dnb_data(dnb_individual: dict):
    prompt_creator = PromptCreator(PerplexityApi())
    return prompt_creator.enrich_dnb_data(str(dnb_individual))

def get_inconsistencies(dnb_individual: dict, matching_list:List[Dict]):
    prompt_creator = PromptCreator(PerplexityApi())
    return prompt_creator.get_inconsistencies(dnb_individual, matching_list)
