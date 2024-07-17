import json
import re



def extract_informations_from_cobol_file_content(cobol_file_content, file_path):
    cobol_file_content_cleaned = clean_cobol_code_line_numbers(cobol_file_content)
    cobol_parsed_dict = parse_cobol_to_json(cobol_file_content_cleaned)
    node_json_list = flatten_parsed_tree(cobol_parsed_dict, file_path)
    return node_json_list


def flatten_parsed_tree(cobol_parsed_dict, file_path):
    code_extraction_elements_list = list()
    for path, value in traverse_json_based_on_keys(cobol_parsed_dict, key_path=[file_path]):
        if isinstance(value,dict) and value["code_structure_type"] in ["DIVISION","SECTION","PARAGRAPH"]:
            value["code_structure_path"] = path
            code_extraction_elements_list.append(value)
    return code_extraction_elements_list


def traverse_json_based_on_keys(json_obj, key_path=None):
    neutral_keys = ["content", "program_id", "perform_calls", "thru_calls", "call_calls"]
    continue_keys = ["paragraphs", "sections"]
    division_key = "DIVISION"

    """
    Traverse all key-value pairs in a JSON object.

    Args:
    json_obj: dict or list, the JSON object to traverse.
    key_path: list, the path of keys leading to the current value.

    Returns:
    Generator yielding tuples of (key_path, value)
    """
    if key_path is None:
        key_path = []

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            current_path = key_path + [key]
            print("traverse_json_based_on_keys key " + str(current_path))
            if division_key in key or key in continue_keys:
                yield from traverse_json_based_on_keys(value, current_path)
            else:
                yield (current_path, value)
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            current_path = key_path + [index]
            print("traverse_json_based_on_keys item " + str(current_path))
            if isinstance(item, (dict, list)):
                yield from traverse_json_based_on_keys(item, current_path)
            else:
                yield (current_path, item)


def traverse_json_based_on_keys1(json_obj, key_path=[]):
    neutral_keys = ["content", "program_id", "perform_calls", "thru_calls", "call_calls"]
    continue_keys = ["paragraphs", "sections"]
    division_key = "DIVISION"

    """
    Traverse all key-value pairs in a JSON object.

    Args:
    json_obj: dict or list, the JSON object to traverse.
    key_path: str, the path of keys leading to the current value.

    Returns:
    None
    """
    if not key_path:
        key_path = list()

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            key_path.append(key)
            # current_path = f"{key_path}.{key}" if key_path else key
            print("traverse_json_based_on_keys key " + str(key_path))
            if division_key in key or key in continue_keys:
                yield from traverse_json_based_on_keys(value, key_path)
                key_path.pop()
            else:
                # self.logger.info(f"Path: {current_path}, Value: {value}")
                yield (key_path, value)
                # key_path.pop()
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            # current_path = f"{key_path}[{index}]"
            print("traverse_json_based_on_keys item " + item)
            if isinstance(item, (dict, list)):
                yield from traverse_json_based_on_keys(item, key_path)
                # key_path.pop()
            else:
                # self.logger.info(f"Path: {current_path}, Value: {item}")
                yield (key_path, item)
                # key_path.pop()


def traverse_json(json_obj, key_path=[]):
    """
    Traverse all key-value pairs in a JSON object.

    Args:
    json_obj: dict or list, the JSON object to traverse.
    key_path: str, the path of keys leading to the current value.

    Returns:
    None
    """
    if not key_path:
        key_path = list()

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            key_path.append(key)
            # current_path = f"{key_path}.{key}" if key_path else key
            if isinstance(value, (dict, list)):
                yield from traverse_json(value, key_path)
                key_path.pop()
            else:
                # self.logger.info(f"Path: {current_path}, Value: {value}")
                yield (key_path, value)
                key_path.pop()
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            # current_path = f"{key_path}[{index}]"
            if isinstance(item, (dict, list)):
                yield from traverse_json(item, key_path)
                # key_path.pop()
            else:
                # self.logger.info(f"Path: {current_path}, Value: {item}")
                yield (key_path, item)
                # key_path.pop()


def remove_not_defined(cobol_parsed_dict):
    """
    Traverse all key-value pairs in a JSON object.
    and remove "not defined" key everywhere.

    Args:
    cobol_parsed_dict: dict or list, the JSON object to traverse.
    key_path: str, the path of keys leading to the current value.

    Returns:
    None
    """
    if isinstance(cobol_parsed_dict, dict):
        for key, value in cobol_parsed_dict.items():
            if isinstance(value, (dict, list)):
                remove_not_defined(value)
    elif isinstance(cobol_parsed_dict, list):
        for index, item in enumerate(cobol_parsed_dict):
            if isinstance(item, (dict, list)):
                remove_not_defined(item)
    else:
        if "not_defined" in cobol_parsed_dict.keys():
            del cobol_parsed_dict["not_defined"]


def clean_cobol_code_line_numbers(code_string):
    """
    This function takes a string representing COBOL code with potential line numbers
    and removes line numbers from the first 6 columns if they are consistent
    for at least the first 5 lines or all lines if there are fewer than 5.
    It then returns the cleaned code as a single string.

    :param code_string: String of COBOL code lines
    :return: String of cleaned COBOL code
    """
    # Split the code string into lines
    code_lines = code_string.splitlines(True)  # Keep newline characters

    # Determine the number of lines to check
    num_lines_to_check = min(5, len(code_lines))

    # Check if the line numbers are consistent in the first 6 columns
    has_line_numbers = all(
        len(line)>5 and line[:6].isdigit() and (line[6] == ' ' or line[6] == '\n') for line in code_lines[:num_lines_to_check]
    )

    # If consistent, remove the line numbers
    if has_line_numbers:
        cleaned_lines = [line[6:] for line in code_lines]
    else:
        cleaned_lines = code_lines

    # Merge the cleaned lines back into a single string
    return ''.join(cleaned_lines)

def extract_matching_regex(regex_pattern, cobol_code_chunk, matching_group = 0):
    matched_strings = list()
    regex_matches = list()
    if cobol_code_chunk:
        regex_matches = list(regex_pattern.finditer(cobol_code_chunk))
    matched_strings = [regex_match.group(matching_group).strip() for regex_match in regex_matches if regex_match]
    return matched_strings


def split_on_matched_strings1(matched_strings, cobol_code_chunk):
    matched_strings = list(set(matched_strings))
    matched_strings = sorted(matched_strings, key=lambda x: cobol_code_chunk.find(x) if x in cobol_code_chunk else float('inf'))

    sub_chunks_dict = dict()

    if len(matched_strings) == 0:
      sub_chunks_dict["not_defined"] = cobol_code_chunk
      return sub_chunks_dict

    pattern = '|'.join(map(re.escape, matched_strings))

    splitted_text = re.split(pattern, cobol_code_chunk)

    matched_strings_new = ["not_defined"] + matched_strings

    for matched_string_idx in range(len(matched_strings_new)):
      if len(splitted_text) > matched_string_idx:
        chunk_key = matched_strings_new[matched_string_idx]
        sub_chunks_dict[chunk_key] = splitted_text[matched_string_idx]
    return sub_chunks_dict


def split_on_matched_strings(matched_strings, cobol_code_chunk):
    if matched_strings and "DIVISION" not in matched_strings[0]:
        matched_strings = list(set(matched_strings))
        matched_strings = sorted(matched_strings, key=lambda x: cobol_code_chunk.find(x) if x in cobol_code_chunk else float('inf'))

    sub_chunks_dict = dict()

    if len(matched_strings) == 0:
      sub_chunks_dict["not_defined"] = cobol_code_chunk
      return sub_chunks_dict

    pattern = '|'.join(map(re.escape, matched_strings))

    splitted_text = re.split(pattern, cobol_code_chunk)

    matched_strings_new = prepare_matched_strings(matched_strings)
    print("matched_strings_new " +str(matched_strings_new))

    for matched_string_idx in range(len(matched_strings_new)):
      if len(splitted_text) > matched_string_idx:
        chunk_key = matched_strings_new[matched_string_idx]
        sub_chunks_dict[chunk_key] = splitted_text[matched_string_idx]
    return sub_chunks_dict


def prepare_matched_strings(matched_strings):
    matched_strings_new = ["not_definedR"] + matched_strings

    divisions_counter = 0
    matched_strings_export = list()
    for matched_string_idx in range(len(matched_strings_new)):

        chunk_key = matched_strings_new[matched_string_idx]

        print("matched_strings_new chunk_key " + chunk_key)

        if "DIVISION" in chunk_key:
            if "USING" in chunk_key:
                chunk_key = chunk_key.replace("USING", "")
            else:
                chunk_key = chunk_key[:-1]

            chunk_key = chunk_key.strip()
            chunk_key = chunk_key + "_" + str(divisions_counter)

            if chunk_key in matched_strings_export:
                chunk_key = chunk_key[:-1]
                chunk_key = chunk_key.strip()
                divisions_counter += 1
                chunk_key = chunk_key + str(divisions_counter)

        else:
            if "SECTION" not in chunk_key:
                pattern_extraction_helper = re.compile(r"\w+(?:-\w+)*\.")
                extracted_paragraphs_name_matched = extract_matching_regex(pattern_extraction_helper,chunk_key)
                if extracted_paragraphs_name_matched:
                    chunk_key = extracted_paragraphs_name_matched[0]
            chunk_key = chunk_key[:-1]
        matched_strings_export.append(chunk_key)
    return matched_strings_export


def extract_single_matching_regex(pattern, cobol_code_chunk):
    match = pattern.search(cobol_code_chunk)
    # Print the result if a match is found
    if match:
        return match.group(1)
    return ""


def parse_cobol_structure(cobol_code_chunk):
    # division_pattern = re.compile(r'\b\w+\s+DIVISION\b.*?\.\s*')
    extracted_divisions = extract_divisions(cobol_code_chunk)

    for extracted_division_name, extracted_division in extracted_divisions.items():

        extracted_sections = extract_sections(extracted_division)

        if "PROCEDURE" in extracted_division_name:

            for extracted_section_name, extracted_section in extracted_sections.items():
                extracted_section_paragraphs = extract_paragraphs(extracted_section)

                if "not_defined" in extracted_section_name:
                    extracted_divisions[extracted_division_name]["paragraphs"] = extracted_section_paragraphs
                else:
                    extracted_sections[extracted_section_name]["paragraphs"] = extracted_section_paragraphs

        extracted_divisions[extracted_division_name]["sections"] = extracted_sections

    return extracted_divisions


def extract_divisions(cobol_code_chunk):


    program_id_match = re.compile(r'PROGRAM-ID\.\s(\w+(?:-\w+)*)')
    # program_id_match = re.compile(r'(?<=PROGRAM-ID\.)\w+(?=\.)')
    # program_id_match = re.compile(r'(?<=PROGRAM-ID\.)\w+(?=\.)')
    division_pattern = re.compile(r'\b\w+\s+DIVISION\b.*?(\.| USING)\s*')

    matched_strings_divisions = extract_matching_regex(division_pattern, cobol_code_chunk)
    extracted_divisions = split_on_matched_strings(matched_strings_divisions, cobol_code_chunk)
    extracted_divisions = {key: {"content": value, "code_structure_type":"DIVISION"} for key, value in extracted_divisions.items()}

    program_id = ""
    for extracted_division_name, extracted_division_content in extracted_divisions.items():

        if "IDENTIFICATION" in extracted_division_name:
            program_id = extract_single_matching_regex(program_id_match, extracted_division_content["content"])
        extracted_divisions[extracted_division_name]["program_id"] = program_id

        if "PROCEDURE" in extracted_division_name:
            program_id = ""

    return extracted_divisions



def extract_sections(extracted_division):

    section_pattern = re.compile(r'\b[\w-]+\s+SECTION\.\s*')

    perform_match = re.compile(r'PERFORM\s(\w+(?:-\w+)*)')
    thru_match = re.compile(r'THRU\s(\w+(?:-\w+)*)')
    call_match = re.compile(r'CALL\s(\w+(?:-\w+)*)')


    extracted_division_content = extracted_division["content"]
    extracted_division_program_id = extracted_division["program_id"]

    matched_strings_sections = extract_matching_regex(section_pattern, extracted_division_content)
    extracted_sections = split_on_matched_strings(matched_strings_sections, extracted_division_content)
    extracted_sections = {key: {"content":value, "program_id": extracted_division_program_id, "code_structure_type":"SECTION"}
                          for key, value in extracted_sections.items()}

    for extracted_section_name, extracted_section in extracted_sections.items():
        extracted_section_content = extracted_section["content"]
        if "not_defined" not in extracted_section_name:
            perform_calls_section = extract_matching_regex(perform_match, extracted_section_content, matching_group = 1)
            thru_calls_section = extract_matching_regex(thru_match, extracted_section_content, matching_group = 1)
            call_calls_section = extract_matching_regex(call_match, extracted_section_content, matching_group = 1)
            extracted_section["perform_calls"] = perform_calls_section
            extracted_section["thru_calls"] = thru_calls_section
            extracted_section["call_calls"] = call_calls_section

    return extracted_sections


def extract_paragraphs(extracted_section):
    # division_pattern = re.compile(r'\b\w+\s+DIVISION\b.*?\.\s*')

    perform_match = re.compile(r'PERFORM\s(\w+(?:-\w+)*)')
    thru_match = re.compile(r'THRU\s(\w+(?:-\w+)*)')
    call_match = re.compile(r'CALL\s(\w+(?:-\w+)*)')

    paragraph_pattern1 = re.compile(r"^\s*\*.*[\n]\s*(\w+(?:-\w+)*\.\s*)$", re.MULTILINE)
    paragraph_pattern2 = re.compile(r"^\s*/.*[\n]\s*(\w+(?:-\w+)*\.\s*)$", re.MULTILINE)
    paragraph_pattern = re.compile(r"(?:\.+|>+|\*?>+|-+)[\s\n]+(\w+(?:-\w+)*)\.")

    extracted_section_content = extracted_section["content"]

    matched_strings_paragraphs = extract_matching_regex(paragraph_pattern, extracted_section_content)

    matched_strings_paragraphs1 = extract_matching_regex(paragraph_pattern1, extracted_section_content)
    matched_strings_paragraphs2 = extract_matching_regex(paragraph_pattern2, extracted_section_content)

    matched_strings_paragraphs.extend(matched_strings_paragraphs1)
    matched_strings_paragraphs.extend(matched_strings_paragraphs2)

    extracted_section_paragraphs = split_on_matched_strings(matched_strings_paragraphs, extracted_section_content)

    for extracted_paragraphs_name, extracted_paragraphs_content in extracted_section_paragraphs.items():

        perform_calls_paragraph = extract_matching_regex(perform_match, extracted_paragraphs_content, matching_group = 1)
        thru_calls_paragraph = extract_matching_regex(thru_match, extracted_paragraphs_content, matching_group = 1)
        call_calls_paragraph = extract_matching_regex(call_match, extracted_paragraphs_content, matching_group = 1)

        extracted_paragraph = {"content": extracted_paragraphs_content,
                               "program_id": extracted_section["program_id"],
                               "perform_calls":perform_calls_paragraph,
                               "thru_calls":thru_calls_paragraph,
                               "call_calls":call_calls_paragraph,
                               "code_structure_type":"PARAGRAPH"}

        extracted_section_paragraphs[extracted_paragraphs_name] = extracted_paragraph

    return extracted_section_paragraphs


def parse_cobol_to_json(cobol_code_chunk):
    parsed_dict = parse_cobol_structure(cobol_code_chunk)
    # json_string = json.dumps(parsed_dict)
    return parsed_dict


def check_empty_code(code_extraction_node):
    words = code_extraction_node.split()
    for word in words:
        if len(word) > 3:
            return True
    return False
