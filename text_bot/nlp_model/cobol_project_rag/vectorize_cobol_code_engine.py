import sys
import json
import ast
sys.path.append("..")

from text_bot.nlp_model.nlp_model import NlpModel
from text_bot.utils import load_documents, save_json_to_file, load_file_json_content, save_json_list_to_separated_files
from text_bot.cobol_code_utils import (parse_cobol_to_json,
                                       clean_cobol_code_line_numbers,
                                       remove_not_defined,
                                       traverse_json,
                                       traverse_json_based_on_keys,
                                       flatten_parsed_tree,
                                       extract_informations_from_cobol_file_content)

from text_bot.graph_db.neo4j_gdb import Neo4jDB
from text_bot.graph_db.neo4j_db_mapper import Neo4jDBMapper

# SENTENCE_MIN_LENGTH = 15
SENTENCE_MIN_LENGTH = 2

from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from text_bot.views.models import CTDocument, \
    CTDocumentSplit, \
    CTDocumentPage, \
    CTDocumentSection, \
    CTDocumentSectionTitle, \
    CTDocumentSectionText, \
    CTDocumentSectionReferences, \
    CTDocumentSectionTopics, \
    CTDocumentSubsection,\
    CTDocumentSubsectionTitle,\
    CTDocumentSubsectionText,\
    CTDocumentSubsectionReferences,\
    CTDocumentSubsectionTopics


from text_bot.nlp_model.cobol_project_rag.cobol_extraction_prompt_creator import CobolExtractionPromptCreator
from text_bot.utils import load_files_contents, get_file_paths, load_file_content, convert_json_string_to_dict
from custom_logger.universal_logger import UniversalLogger


MAX_CHUNK_SIZE = 500
MAX_CHUNK_OVERLAP_SIZE = 250
MAX_SEMANTIC_CHUNK_SIZE = 1000
MAX_SEMANTIC_CHUNK_OVERLAP_SIZE = 500
MAX_PAGE_SIZE = 5500

HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]

class VectorizeCobolCodeEngine:


    def __init__(self, nlp_model :NlpModel):
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)
        self.model = nlp_model
        self.prompt_creator = CobolExtractionPromptCreator(nlp_model)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_CHUNK_SIZE, chunk_overlap=MAX_CHUNK_OVERLAP_SIZE)
        self.semantic_text_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_SEMANTIC_CHUNK_SIZE, chunk_overlap=MAX_SEMANTIC_CHUNK_OVERLAP_SIZE)
        self.pages_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_PAGE_SIZE, chunk_overlap=0)
        self.markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
        self.neo4j_db = Neo4jDB()
        self.neo4j_db_mapper = Neo4jDBMapper()



    def add_frd_extraction(self, cobol_extraction_json_list):
        code_extraction_node_list = list()

        for cobol_extraction_json in cobol_extraction_json_list:
            cobol_extraction_json = self.prepare_frd_node(cobol_extraction_json)
            code_semantic_extraction_json = self.prompt_creator.create_frd(cobol_extraction_json)
            code_extraction_node_list.append(code_semantic_extraction_json)

        save_json_to_file(code_extraction_node_list, "json_export/json_frd")
        return code_extraction_node_list


    def add_dependencies_summarization(self, cobol_extraction_json_list):
        # project_root_path = "json_export/json_example_20240625_205528.json"
        # cobol_extraction_json_list = load_file_json_content(project_root_path)

        code_extraction_node_list = list()

        for cobol_extraction_json in cobol_extraction_json_list:
            children_nodes_prepared_list = list()
            dependency_nodes_prepared_list = list()
            if "PROCEDURE" in cobol_extraction_json["node_name"]:
                children_nodes_names_list = cobol_extraction_json.get("children_nodes", [])
                external_dependencies_names_list = cobol_extraction_json.get("external_dependencies", [])
                internal_dependencies_names_list = cobol_extraction_json.get("internal_dependencies", [])
                dependency_names_list =  external_dependencies_names_list+internal_dependencies_names_list

                for cobol_extraction_json_new in cobol_extraction_json_list:
                    if cobol_extraction_json_new["node_name"] in children_nodes_names_list:
                        children_nodes_prepared_list.append(cobol_extraction_json_new)
                    if cobol_extraction_json_new["node_name"] in dependency_names_list:
                        dependency_nodes_prepared_list.append(cobol_extraction_json_new)

                single_node_json = self.add_llm_summarization(cobol_extraction_json,
                                                              children_nodes_prepared_list,
                                                              dependency_nodes_prepared_list)
                code_extraction_node_list.append(single_node_json)

        cobol_extraction_json = dict()
        cobol_extraction_json["node_name"] = "OVERALL"
        cobol_extraction_json["code"] = ""
        dependency_nodes_prepared_list = None
        single_node_json = self.add_llm_summarization(cobol_extraction_json,
                                                      code_extraction_node_list,
                                                      dependency_nodes_prepared_list)
        code_extraction_node_list.append(single_node_json)


        save_json_to_file(code_extraction_node_list, "json_export/json_summarization")
        return code_extraction_node_list




    def load_cobol_project_files(self, project_root_path):
        cobol_extraction_json_list = self.load_cobol_project_content(project_root_path)

        # project_root_path = "json_export/json_example_20240627_195230.json"
        # cobol_extraction_json_list = load_file_json_content(project_root_path)

        self.add_cobol_project_nodes(cobol_extraction_json_list)
        # cobol_extraction_json_list = self.add_dependencies_summarization(cobol_extraction_json_list)
        # cobol_extraction_json_list = self.add_frd_extraction(cobol_extraction_json_list)
        # save_json_list_to_separated_files(cobol_extraction_json_list, "json_export")



    def add_cobol_project_nodes(self, cobol_extraction_json_list):

        variables_list = self.neo4j_db_mapper.extract_all_variables_list(cobol_extraction_json_list)

        for node_json in variables_list:
            node_json["node_type"] = "variable"
            node_json["node_name"] = node_json["NAME"]
            properties = {"DESCRIPTION": node_json["DESCRIPTION"]}
            self.neo4j_db.create_node(node_json, properties)


        for node_json in cobol_extraction_json_list:
            if "PROCEDURE" in node_json["division_name"]:

                print("node_name"+node_json["node_name"])

                if node_json["starting_point"]:
                    node_json["node_type"] = "MAIN"

                keys_path = ["llm_extraction", "procedure_division", "procedures_list", 0, "BUSSINES_LOGIC_DESCRIPTION"]
                node_json["BUSSINES_LOGIC_DESCRIPTION"] = self.neo4j_db_mapper.safe_get(node_json, keys_path, default=[])

                keys_path = ["llm_extraction", "procedure_division", "procedures_list", 0, "FUNCTIONAL_LOGIC_FEATURES_LIST"]
                node_json["FUNCTIONAL_LOGIC_FEATURES_LIST"] = self.neo4j_db_mapper.safe_get(node_json, keys_path, default=[])

                properties = {"BUSSINES_LOGIC_DESCRIPTION": node_json["BUSSINES_LOGIC_DESCRIPTION"],
                              "FUNCTIONAL_LOGIC_FEATURES_LIST": node_json["FUNCTIONAL_LOGIC_FEATURES_LIST"],
                              "code":node_json["code"],
                              "code_structure_type": node_json["code_structure_type"]
                              }
                self.neo4j_db.create_node(node_json, properties)


        for node_json in cobol_extraction_json_list:
            if "PROCEDURE" in node_json["division_name"]:

                # "meta_divisions": [
                #     "IDENTIFICATION DIVISION_2",
                #     "DATA DIVISION_2"
                # ],

                meta_divisions = [{"node_name": dependency_name, "node_type": "code_block", "program_id":node_json["program_id"]}
                                         for dependency_name in node_json["internal_dependencies"]]
                if meta_divisions:
                    self.neo4j_db.create_edges_on_parent( node_json, meta_divisions, "usage")

                variables_keys_path = ["llm_extraction", "procedure_division", "procedures_list", 0, "variables_list"]
                variables = self.neo4j_db_mapper.safe_get(node_json, variables_keys_path, default=[])

                variables = [{"node_name":variable["NAME"], "node_type":"variable", "program_id":node_json["program_id"]}
                             for variable in variables]
                if variables:
                    self.neo4j_db.create_edges_on_parent( node_json, variables, "usage")

                dependencies_keys_path = ["llm_extraction", "procedure_division", "procedures_list", 0, "dependencies_list"]
                dependencies_list = self.neo4j_db_mapper.safe_get(node_json, dependencies_keys_path, default=[])

                dependencies_list = [{"node_name":dependency["dependency_name"], "node_type":"code_block", "program_id":node_json["program_id"]}
                                     for dependency in dependencies_list]
                if variables:
                    self.neo4j_db.create_edges_on_parent( node_json, dependencies_list, "perform")



                external_dependencies = [{"node_name":dependency_name, "node_type":"code_block"}
                                         for dependency_name in node_json["external_dependencies"]]
                if node_json["external_dependencies"]:
                    self.neo4j_db.create_edges_on_parent( node_json, external_dependencies, "call")


                internal_dependencies = [{"node_name": dependency_name, "node_type":"code_block", "program_id":node_json["program_id"]}
                                         for dependency_name in node_json["internal_dependencies"]]
                if node_json["internal_dependencies"]:
                    self.neo4j_db.create_edges_on_parent( node_json, internal_dependencies, "perform")


                children_nodes = [{"node_name": dependency_name, "node_type":"code_block", "program_id":node_json["program_id"]}
                                         for dependency_name in node_json["children_nodes"]]
                if node_json["children_nodes"]:
                    self.neo4j_db.create_edges_on_parent( node_json, children_nodes, "child")



    def load_cobol_project_content(self, project_root_path):
        self.logger.info("project_root_path: " + str(project_root_path))
        file_path_list = get_file_paths(project_root_path)
        self.logger.info("file_path_list: " + str(file_path_list))
        code_extraction_node_list = list()
        for file_path in file_path_list:
            self.logger.info("file_path: " + file_path)
            cobol_file_content = load_file_content(file_path)

            node_json_list = extract_informations_from_cobol_file_content(cobol_file_content, file_path)
            node_json_list = self.neo4j_db_mapper.mapp_parser_nodes_to_neo4j_prepared_nodes(node_json_list)
            node_json_list = self.neo4j_db_mapper.remove_redudant_code_chunks(node_json_list)

            for node_json in node_json_list:
                single_node_json = self.add_llm_extraction(node_json)

                self.logger.info("extracted info"+str(single_node_json))
                code_extraction_node_list.append(single_node_json)

        code_extraction_node_list = self.neo4j_db_mapper.recognize_external_call_variables(code_extraction_node_list)
        code_extraction_node_list = self.neo4j_db_mapper.add_dependent_divisions(code_extraction_node_list)
        code_extraction_node_list = self.neo4j_db_mapper.filter_out_no_code_chunks(code_extraction_node_list)
        code_extraction_node_list = self.neo4j_db_mapper.recognize_external_dependencies(code_extraction_node_list)

        # code_extraction_node_list = self.neo4j_db_mapper.find_starting_node(code_extraction_node_list)

        code_extraction_node_list = self.neo4j_db_mapper.add_children_to_nodes(code_extraction_node_list)
        save_json_to_file(code_extraction_node_list, "json_export/json_example" )
        return code_extraction_node_list


    def add_llm_extraction(self, single_node_json):
        print("add_llm_extraction")
        division_name = single_node_json["code_structure_path"][1]
        code_chunk = single_node_json.get("code",None)
        code_semantic_extraction_json = ""
        if code_chunk:
            code_semantic_extraction_json = self.prompt_creator.extract_cobol_chunk_info(division_name, code_chunk)
        single_node_json["llm_extraction"] = code_semantic_extraction_json
        return single_node_json

    def add_llm_summarization(self, single_node_json,
                                children_description_extraction_list,
                                dependencies_description_extraction_list):

        print("add_llm_summarization")

        current_cobol_code_extraction = ""
        if single_node_json:
            current_cobol_code_extraction = self.prepare_summarization_node(single_node_json)

        children_description_prepared_list = []
        if children_description_extraction_list:
            children_description_prepared_list = list()
            for child in children_description_extraction_list:
                children_description_prepared_list = self.prepare_summarization_node(child)

        dependencies_description_prepared_list = []
        if dependencies_description_extraction_list:
            dependencies_description_prepared_list = list()
            for dependency in dependencies_description_extraction_list:
                dependencies_description_prepared_list = self.prepare_summarization_node(dependency)

        code_semantic_extraction_json = self.prompt_creator.summarize_dependencies_info(current_cobol_code_extraction,
                                                                                        children_description_prepared_list,
                                                                                        dependencies_description_prepared_list)

        single_node_json["llm_summarization"] = code_semantic_extraction_json
        return single_node_json


    def prepare_summarization_node(self, single_node_json):
        print("single_node_json " + str(single_node_json))
        current_cobol_code_extraction = dict()
        current_cobol_code_extraction["code"] = single_node_json["code"]
        dependencies_keys_path = ["llm_extraction", "procedure_division", "procedures_list", 0]
        procedures_extraction = self.neo4j_db_mapper.safe_get(single_node_json, dependencies_keys_path, default=[])

        print("procedures_extraction "+str(procedures_extraction))

        if procedures_extraction:
            current_cobol_code_extraction["DEV_COMMENTS"] = procedures_extraction["DEV_COMMENTS"]
            current_cobol_code_extraction["BUSSINES_LOGIC_DESCRIPTION"] = procedures_extraction["BUSSINES_LOGIC_DESCRIPTION"]
            current_cobol_code_extraction["BUSSINES_LOGIC_FEATURES_LIST"] = procedures_extraction["BUSSINES_LOGIC_FEATURES_LIST"]
            current_cobol_code_extraction["FUNCTIONAL_LOGIC_DESCRIPTION"] = procedures_extraction["FUNCTIONAL_LOGIC_DESCRIPTION"]
            current_cobol_code_extraction["FUNCTIONAL_LOGIC_FEATURES_LIST"] = procedures_extraction["FUNCTIONAL_LOGIC_FEATURES_LIST"]
            current_cobol_code_extraction["WORK_FLOW"] = procedures_extraction["WORK_FLOW"]
            current_cobol_code_extraction["variables_list"] = procedures_extraction["variables_list"]



        llm_summarization = single_node_json.get("llm_summarization",None)

        print("llm_summarization "+str(llm_summarization))

        if llm_summarization and isinstance(llm_summarization, dict):
            current_cobol_code_extraction["CHILD_NODES_BUSSINES_LOGIC_SUMMARIZATION"] = llm_summarization["CHILD_NODES_BUSSINES_LOGIC_SUMMARIZATION"]
            current_cobol_code_extraction["CHILD_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION"] = llm_summarization["CHILD_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION"]
            current_cobol_code_extraction["DEPENDENCY_NODES_BUSSINES_LOGIC_SUMMARIZATION"] = llm_summarization["DEPENDENCY_NODES_BUSSINES_LOGIC_SUMMARIZATION"]
            current_cobol_code_extraction["DEPENDENCY_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION"] = llm_summarization["DEPENDENCY_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION"]
            current_cobol_code_extraction["GENERAL_INPUT_AND_OUTPUT_VARIABLES_LIST"] = llm_summarization["GENERAL_INPUT_AND_OUTPUT_VARIABLES_LIST"]
            current_cobol_code_extraction["OVERALL_WORK_FLOW"] = llm_summarization["OVERALL_WORK_FLOW"]

        return current_cobol_code_extraction

    def prepare_frd_node(self, single_node_json):
        print("single_node_json " + str(single_node_json))
        current_cobol_code_extraction = dict()
        dependencies_keys_path = ["llm_extraction", "procedure_division", "procedures_list", 0]
        procedures_extraction = self.neo4j_db_mapper.safe_get(single_node_json, dependencies_keys_path, default=[])

        if procedures_extraction:
            current_cobol_code_extraction["DEV_COMMENTS"] = procedures_extraction["DEV_COMMENTS"]
            current_cobol_code_extraction["BUSSINES_LOGIC_DESCRIPTION"] = procedures_extraction[
                "BUSSINES_LOGIC_DESCRIPTION"]
            current_cobol_code_extraction["BUSSINES_LOGIC_FEATURES_LIST"] = procedures_extraction[
                "BUSSINES_LOGIC_FEATURES_LIST"]
            current_cobol_code_extraction["FUNCTIONAL_LOGIC_DESCRIPTION"] = procedures_extraction[
                "FUNCTIONAL_LOGIC_DESCRIPTION"]
            current_cobol_code_extraction["FUNCTIONAL_LOGIC_FEATURES_LIST"] = procedures_extraction[
                "FUNCTIONAL_LOGIC_FEATURES_LIST"]
            current_cobol_code_extraction["WORK_FLOW"] = procedures_extraction["WORK_FLOW"]
            current_cobol_code_extraction["variables_list"] = procedures_extraction["variables_list"]
            current_cobol_code_extraction["errors_edge_cases_list"] = procedures_extraction["errors_edge_cases_list"]
            current_cobol_code_extraction["declaratives"] = procedures_extraction["declaratives"]
            current_cobol_code_extraction["dependencies_list"] = procedures_extraction["dependencies_list"]


        llm_summarization = single_node_json.get("llm_summarization", None)

        if llm_summarization and isinstance(llm_summarization, dict):
            current_cobol_code_extraction["CHILD_NODES_BUSSINES_LOGIC_SUMMARIZATION"] = llm_summarization[
                "CHILD_NODES_BUSSINES_LOGIC_SUMMARIZATION"]
            current_cobol_code_extraction["CHILD_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION"] = llm_summarization[
                "CHILD_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION"]
            current_cobol_code_extraction["DEPENDENCY_NODES_BUSSINES_LOGIC_SUMMARIZATION"] = llm_summarization[
                "DEPENDENCY_NODES_BUSSINES_LOGIC_SUMMARIZATION"]
            current_cobol_code_extraction["DEPENDENCY_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION"] = llm_summarization[
                "DEPENDENCY_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION"]
            current_cobol_code_extraction["GENERAL_INPUT_AND_OUTPUT_VARIABLES_LIST"] = llm_summarization[
                "GENERAL_INPUT_AND_OUTPUT_VARIABLES_LIST"]
            current_cobol_code_extraction["OVERALL_WORK_FLOW"] = llm_summarization["OVERALL_WORK_FLOW"]

        return current_cobol_code_extraction