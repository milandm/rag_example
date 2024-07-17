from neo4j import GraphDatabase
from text_bot.utils import load_documents, save_json_to_file, load_file_json_content
from custom_logger.universal_logger import UniversalLogger
from text_bot.graph_db.neo4j_transactions import (add_node,
                                                  add_node_with_properties,
                                                  add_edge,
                                                  handle_properties,
                                                  edit_node,
                                                  edit_edge,
                                                  delete_node,
                                                  delete_edge,
                                                  delete_all_nodes)
from text_bot.nlp_model.config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD
)
from text_bot.cobol_code_utils import extract_single_matching_regex, check_empty_code, extract_matching_regex
import json
import ast
from text_bot.utils import load_files_contents, get_file_paths, load_file_content, convert_json_string_to_dict
import re

properties_to_use = ['general_info', 'type', 'code']

class Neo4jDBMapper:


    def __init__(self):
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)


    def get_node_dependencies(self, cobol_extraction_node):
        children_nodes = dict()
        procedure_name = cobol_extraction_node["procedure_name"]
        if "PROCEDURE" in procedure_name:
            llm_extraction = cobol_extraction_node.get("llm_extraction", None)
            self.logger.info("llm_extraction type " + str(type(llm_extraction)))
            if isinstance(llm_extraction, str):
                try:
                    llm_extraction = json.loads(llm_extraction)
                except json.JSONDecodeError as e:
                    self.logger.error(f"Error converting string to dictionary: {e}")
                # llm_extraction = ast.literal_eval(llm_extraction)
                # # llm_extraction = json.loads(llm_extraction)

            # self.logger.info("llm_extraction "+str(llm_extraction))
            if llm_extraction and isinstance(llm_extraction, dict):
                procedure_division = llm_extraction.get("procedure_division", None)
                if procedure_division:
                    procedures_list = procedure_division.get("procedures_list", None)
                    if procedures_list:

                        variables_list = procedures_list[0].get("variables_list", [])
                        new_variables_list = list()
                        for variable in variables_list:
                            new_variable = dict()
                            new_variable["node_name"] = variable["NAME"]
                            new_variable["node_type"] = "variable"
                            new_variable["dependencies_list"] = []
                            new_variables_list.append(new_variable)

                        dependencies_list = procedures_list[0].get("dependencies_list", [])
                        new_dependencies_list = list()
                        for dependency in dependencies_list:
                            new_dependency = dict()
                            new_dependency["node_name"] = dependency["dependency_name"]
                            new_dependency["node_type"] = "code_block"
                            new_dependency["dependencies_list"] = []
                            new_dependencies_list.append(new_dependency)

                        children_nodes["variables"] = new_variables_list
                        children_nodes["dependencies"] = new_dependencies_list
                        return children_nodes

        children_nodes["variables"] = []
        children_nodes["dependencies"] = []
        return children_nodes

    def merge_llm_and_parser_extraction(self, project_root_path):
        project_root_path = "json_export/"
        file_path_list = get_file_paths(project_root_path, extensions="json")
        self.logger.info("file_path_list: " + str(file_path_list))
        json_files_list = list()
        for file_path in file_path_list:
            cobol_extraction_json_list = load_file_json_content(file_path)
            json_files_list.append(cobol_extraction_json_list)
        for index, node_extraction in enumerate(json_files_list[1]):
            # if len(json_files_list[1])>index:
            json_files_list[0][index]["llm_extraction"] = node_extraction["llm_extraction"]
        save_json_to_file(json_files_list[0], "json_export/json_merged")


    def extract_all_variables_list(self, code_extraction_node_list):
        # Keys path to the desired value
        keys_path = ["llm_extraction", "procedure_division", "procedures_list", 0, "variables_list"]
        variables_list = dict()
        for json_node in code_extraction_node_list:
            if "PROCEDURE" in json_node["division_name"]:
                # current_variables_list = json_node["llm_extraction"]["procedure_division"]["procedures_list"][0]["variables_list"]
                # Safe access using the helper function
                current_variables_list = self.safe_get(json_node, keys_path, default=[])
                for variable in current_variables_list:
                    variable["program_id"] = json_node["program_id"]
                    variables_list[variable["NAME"]] = variable
        return variables_list.values()

    def safe_get(self, dictionary, keys, default=None):
        for key in keys:
            try:
                dictionary = dictionary[key]
            except (KeyError, TypeError, IndexError):
                return default
        return dictionary

    # TODO
    # dodati tip code chunka, moze sve da bude code_block
    def add_children_to_nodes(self, code_extraction_node_list):
        procedures_dict = dict()
        for json_node in code_extraction_node_list:
            current_program_id = json_node["program_id"]
            current_parent_node_name = json_node.get("parent_node_name", None)
            current_node_name = json_node["node_name"]

            if not procedures_dict.get(current_program_id, None):
                procedures_dict[current_program_id] = dict()

            if not procedures_dict[current_program_id].get(current_parent_node_name, None):
                procedures_dict[current_program_id][current_parent_node_name] = list()

            if (current_node_name != current_parent_node_name
                    and current_node_name not in procedures_dict[current_program_id][current_parent_node_name]):
                procedures_dict[current_program_id][current_parent_node_name].append(current_node_name)


        for json_node in code_extraction_node_list:
            current_program_id = json_node["program_id"]
            current_node_name = json_node["node_name"]
            current_parent_node_name = json_node.get("parent_node_name", None)

            if procedures_dict.get(current_program_id, None):
                json_node["children_nodes"] = procedures_dict[current_program_id].get(current_node_name, [])

        return code_extraction_node_list


    # TODO
    def find_starting_node(self, code_extraction_node_list):

        external_calls_to_procedure_by_program_id = dict()
        external_calls_to_procedure_by_node_name_id = dict()

        for code_extraction_node in code_extraction_node_list:
            if ("PROCEDURE" in code_extraction_node["node_name"]
                    and "DIVISION" in code_extraction_node["code_structure_type"]):
                for code_extraction_node_new in code_extraction_node_list:
                    if ("PROCEDURE" in code_extraction_node["node_name"]
                            and "DIVISION" in code_extraction_node["code_structure_type"]):
                            if code_extraction_node["node_name"] in code_extraction_node_new["external_dependencies"]:
                                external_calls_to_procedure_by_program_id[code_extraction_node["program_id"]] = code_extraction_node_new["program_id"]
                                external_calls_to_procedure_by_node_name_id[code_extraction_node["node_name"]] = code_extraction_node_new["node_name"]

        for code_extraction_node in code_extraction_node_list:
            if ("PROCEDURE" in code_extraction_node["node_name"]
                    and "DIVISION" in code_extraction_node["code_structure_type"]):
                node_name = code_extraction_node["node_name"]
                code_extraction_node["order_number"] = int(node_name.replace("PROCEDURE DIVISION_", ""))


                if not external_calls_to_procedure_by_program_id.get(code_extraction_node["program_id"]):
                    code_extraction_node["order_number"] = int(node_name.replace("PROCEDURE DIVISION_", ""))

                    code_extraction_node["starting_point"] = True





    def recognize_external_dependencies(self, code_extraction_node_list):
        program_id_procedure = dict()
        for code_extraction_node in code_extraction_node_list:
            if ("PROCEDURE" in code_extraction_node["node_name"]
                    and "DIVISION" in code_extraction_node["code_structure_type"]):
                program_id_procedure[code_extraction_node["program_id"]] = code_extraction_node["node_name"]

        for code_extraction_node in code_extraction_node_list:
            if ("DATA" in code_extraction_node["node_name"]
                and "DIVISION" in code_extraction_node["code_structure_type"]):
                for variable_name, program_id in code_extraction_node["program_id_variables_list"].itmes():
                    external_dependency = program_id_procedure[program_id]
                    if not code_extraction_node.get("external_dependencies", None):
                        code_extraction_node["external_dependencies"] = list()
                    code_extraction_node["external_dependencies"].append(external_dependency)

        return code_extraction_node_list



    def recognize_external_call_variables(self, code_extraction_node_list):

        base_pattern = r"01\s+(\w+)\s+PIC\s+X\(\d+\)\s+VALUE\s+'{}'\."

        all_program_ids = list()
        for code_extraction_node in code_extraction_node_list:
            all_program_ids.append(code_extraction_node["program_id"])

        all_program_ids = list(set(all_program_ids))
        for code_extraction_node in code_extraction_node_list:
            if ("DATA" in code_extraction_node["node_name"]
                    and "DIVISION" in code_extraction_node["code_structure_type"]):
                code_extraction_node["program_id_variables_list"] = dict()
                for program_id in all_program_ids:
                    regex = """01\s+(.+?)\s+PIC\s+X\(\d+\)\s+VALUE\s+'"""+program_id+"""'?\."""
                    base_pattern = re.compile(regex)
                    variable_sentences = extract_matching_regex(base_pattern, code_extraction_node["code"])
                    for variable_sentence in variable_sentences:
                        words = variable_sentence.split()
                        if len(words) >= 2:
                            code_extraction_node["program_id_variables_list"][words[1]] = program_id
        return code_extraction_node_list

    def add_dependent_divisions(self, code_extraction_node_list):
        procedures_dict = dict()
        for json_node in code_extraction_node_list:
            current_program_id = json_node["program_id"]
            current_node_name = json_node["node_name"]

            if not procedures_dict.get(current_program_id, None):
                procedures_dict[current_program_id] = list()

            if (current_node_name
                    and "DIVISION" in current_node_name
                    and "PROCEDURE" not in current_node_name
                    and current_node_name not in procedures_dict[current_program_id]):
                procedures_dict[current_program_id].append(current_node_name)

        print("procedures_dict " + str(procedures_dict))

        for json_node in code_extraction_node_list:
            current_program_id = json_node["program_id"]
            current_node_name = json_node["node_name"]

            if "PROCEDURE" in current_node_name:
                if procedures_dict.get(current_program_id, None):
                    json_node["meta_divisions"] = procedures_dict.get(current_program_id, [])

        return code_extraction_node_list

    def filter_out_no_code_chunks(self, code_extraction_node_list):
        condition = lambda code_extraction_node: (
                code_extraction_node.get("meta_divisions", None)
                or code_extraction_node.get("children_nodes", None)
                or check_empty_code(code_extraction_node["code"])
        )
        return [code_extraction_node for code_extraction_node in code_extraction_node_list if
                condition(code_extraction_node)]


    def remove_redudant_code_chunks(self,node_json_list):
        current_not_defined_node_index = None
        for index,node_json in enumerate(node_json_list):
            node_json_code = node_json["code"]
            if node_json["node_name"] == "not_defined":
                current_not_defined_node_index = index
            elif node_json_code:
                node_json_list[current_not_defined_node_index]["code"] = node_json_list[current_not_defined_node_index]["code"].replace(node_json_code, "")
        return node_json_list

    def mapp_parser_nodes_to_neo4j_prepared_nodes(self, code_extraction_node_list):
        return [self.prepare_single_node(code_extraction_node) for code_extraction_node in code_extraction_node_list]

    def prepare_single_node(self, node_json):
        print("node_json "+str(node_json))
        json_structure_path = list(node_json["code_structure_path"])

        starting_point = False
        file_path = json_structure_path[0]
        program_id = node_json["program_id"]
        code_structure_type = node_json["code_structure_type"]
        node_name = self.get_node_name(json_structure_path)
        if not program_id:
            program_id = file_path
            if code_structure_type == "DIVISION" and "PROCEDURE" in node_name:
                starting_point = True

        node_name = self.get_node_name(json_structure_path)
        if "DIVISION" in node_name:
            code_structure_type = "DIVISION"

        # node_json["node_type"]?maybe to add additional field that show which type of code structure chunk procedure, paragraph, section, MAIN
        # node_type = "code_block"  # node_json["node_type"]?maybe to add additional field that show which type of code structure chnuk

        full_code_semantic_extraction_json = dict()
        # if not isinstance(code_semantic_extraction_json, dict):
        #     code_semantic_extraction_json = convert_json_string_to_dict(code_semantic_extraction_json)
        full_code_semantic_extraction_json["starting_point"] = starting_point
        full_code_semantic_extraction_json["code_structure_path"] = json_structure_path
        full_code_semantic_extraction_json["file_path"] = self.get_node_file_path(json_structure_path)
        full_code_semantic_extraction_json["parent_node_name"] = self.get_parent_node_name(json_structure_path)
        full_code_semantic_extraction_json["division_name"] = self.get_node_division_name(json_structure_path)
        full_code_semantic_extraction_json["node_name"] = self.get_node_name(json_structure_path)

        # TODO
        # code_block type for all code chunks
        full_code_semantic_extraction_json["code_structure_type"] = code_structure_type
        full_code_semantic_extraction_json["node_type"] = "code_block"
        full_code_semantic_extraction_json["code"] = node_json.get("content","")
        full_code_semantic_extraction_json["program_id"] = program_id
        full_code_semantic_extraction_json["external_dependencies"] = node_json.get("call_calls",[])
        full_code_semantic_extraction_json["internal_dependencies"] = node_json.get("perform_calls",[])+node_json.get("thru_calls",[])

        return full_code_semantic_extraction_json


    def get_node_file_path(self, json_structure_path):
        if not json_structure_path:
            return ""
        return json_structure_path[0]


    def get_parent_node_name(self, json_structure_path):
        if not json_structure_path:
            return ""
        parent_node_name = ""
        if len(json_structure_path) > 2:
            parent_node_name = json_structure_path[-3]
        else:
            parent_node_name = json_structure_path[-1]
        return parent_node_name

    def get_node_division_name(self, json_structure_path):
        if not json_structure_path:
            return ""
        if len(json_structure_path) > 1:
            return json_structure_path[1]
        else:
            json_structure_path[0]


    def get_node_name(self, json_structure_path):
        if not json_structure_path:
            return ""
        node_name = json_structure_path[-1]
        if node_name == "not_defined":
            return self.get_parent_node_name(json_structure_path)
        else:
            return node_name







