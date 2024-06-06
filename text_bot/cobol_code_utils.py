import json
import re


def parse_cobol_to_json(cobol_code):

    divisions = {
        'IDENTIFICATION DIVISION.': {},
        'ENVIRONMENT DIVISION.': {
            'CONFIGURATION SECTION': {},
            'INPUT-OUTPUT SECTION': {},
        },
        'DATA DIVISION.': {
            'FILE SECTION': {},
            'WORKING-STORAGE SECTION': {},
            'WORKING-STORAGE VARIABLES': {},
            'LOCAL-STORAGE SECTION': {},
            'LOCAL-STORAGE VARIABLES': {},
            'LINKAGE SECTION': {},
            'LINKAGE SECTION VARIABLES': {},
            'COMMUNICATION SECTION': {},
            'REPORT SECTION': {},
            'SCREEN SECTION': {}
        },
        'PROCEDURE DIVISION.': {}
    }


def parse_cobol_structure(cobol_code):
    """'IDENTIFICATION DIVISION.': {},
    'ENVIRONMENT DIVISION.': {
        'CONFIGURATION SECTION': {},
        'INPUT-OUTPUT SECTION': {},
    },
    'DATA DIVISION.': {
        'FILE SECTION': {},
        'WORKING-STORAGE SECTION': {},
        'WORKING-STORAGE VARIABLES': {},
        'LOCAL-STORAGE SECTION': {},
        'LOCAL-STORAGE VARIABLES': {},
        'LINKAGE SECTION': {},
        'LINKAGE SECTION VARIABLES': {},
        'COMMUNICATION SECTION': {},
        'REPORT SECTION': {},
        'SCREEN SECTION': {}
    },

    PARA-1.
    MAIN-PARA.
    SOMENAME.# this is also PROCEDURE.
    # procedure could be defined the same way as paragraph,
    # but if that part of code contains sections, then it is procedure,
    # because paragraph cant contain sections, but section can contain paragraphs

    'PROCEDURE DIVISION.': {
    'PROCEDURES': [],
    'SECTIONS': [],
    }"""
    divisions_list = cobol_code.split('DIVISION.')


def extract_matching_regex(regex_pattern, cobol_code_chunk):
    matched_strings = list()
    regex_matches = list()
    if cobol_code_chunk:
      regex_matches = list(regex_pattern.finditer(cobol_code_chunk))
    matched_strings = [regex_match.group(0).strip() for regex_match in regex_matches if regex_match]
    return matched_strings

def split_on_matched_strings(matched_strings, cobol_code_chunk):

    matched_strings = list(set(matched_strings))
    matched_strings = sorted(matched_strings, key=lambda x: cobol_code_chunk.find(x) if x in cobol_code_chunk else float('inf'))

    print("sorted matched_strings "+str(matched_strings))

    sub_chunks_dict = dict()

    if len(matched_strings) == 0:
      sub_chunks_dict["not_defined"] = cobol_code_chunk
      return sub_chunks_dict

    pattern = '|'.join(map(re.escape, matched_strings))

    splitted_text = re.split(pattern, cobol_code_chunk)
    # print("splitted_text "+str(splitted_text))

    # print("matched_strings formatted"+str(matched_strings))
    print("splitted_text "+str(splitted_text))

    matched_strings_new = ["not_defined"] + matched_strings

    for matched_string_idx in range(len(matched_strings_new)):
      if len(splitted_text) > matched_string_idx:
        sub_chunks_dict[matched_strings_new[matched_string_idx]] = splitted_text[matched_string_idx]

    return sub_chunks_dict

def split_on_matched_strings2(matched_strings, cobol_code_chunk):
    # Sort substrings by their first occurrence in the string
    # substrings = sorted(substrings, key=lambda x: main_string.find(x) if x in main_string else float('inf'))

    print("split_on_metched_strings matched_strings "+str(matched_strings))

    # Create a dictionary to hold the results
    sub_chunks_dict = {}

    if len(matched_strings) == 0:
      sub_chunks_dict["not_defined"] = cobol_code_chunk
      return sub_chunks_dict

    end_index = cobol_code_chunk.find(matched_strings[0])
    sub_chunks_dict["not_defined"] = cobol_code_chunk[:end_index].strip()

    print("split_on_metched_strings sub_chunks_dict "+str(sub_chunks_dict))


    # Find all the substrings in the main string and create the dictionary
    for i, substring in enumerate(matched_strings):
        if substring in cobol_code_chunk:
            start_index = cobol_code_chunk.find(substring) + len(substring)
            # Look for the next substring's start index to slice till there
            end_index = None
            if i < len(matched_strings) - 1:
                next_substring = matched_strings[i + 1]
                if next_substring in cobol_code_chunk:
                    end_index = cobol_code_chunk.find(next_substring)
                    sub_chunks_dict[substring] = cobol_code_chunk[start_index:end_index].strip()
            else:
              sub_chunks_dict[substring] = cobol_code_chunk[start_index:].strip()
            # Slice the string and store it in the dictionary
            sub_chunks_dict[substring] = cobol_code_chunk[start_index:end_index].strip()

    return sub_chunks_dict


def split_on_matched_strings1(matched_strings, cobol_code_chunk):

    matched_strings = sorted(matched_strings, key=lambda x: cobol_code_chunk.find(x) if x in cobol_code_chunk else float('inf'))

    print("matched_strings "+str(matched_strings))
    # print("cobol_code_chunk "+str(cobol_code_chunk))

    # Create a dictionary to hold the results
    sub_chunks_dict = {}

    # If no matched strings are provided, return the whole chunk as 'not_defined'
    if len(matched_strings) == 0:
        sub_chunks_dict["not_defined"] = cobol_code_chunk
        return sub_chunks_dict

    # Initialize the start index for the first slice
    start_index = 0
    last_substring = ""

    end_index = cobol_code_chunk.find(matched_strings[0])
    start_index = end_index + len(matched_strings[0])
    # Add the remaining part of the string after the last matched substring
    sub_chunks_dict["not_defined"] = cobol_code_chunk[:start_index].strip()

    # Iterate over the matched strings and split accordingly
    for i, substring in enumerate(matched_strings):
        if substring not in sub_chunks_dict.keys():
          if substring in cobol_code_chunk:
              end_index = cobol_code_chunk.find(substring)
              # Slice from the start_index to the current substring's start index
              sub_chunks_dict[substring] = cobol_code_chunk[start_index:end_index].strip()
              # Move the start index to the end of the current substring
              start_index = end_index + len(substring)
              last_substring = substring

    # Add the remaining part of the string after the last matched substring
    sub_chunks_dict[last_substring] = cobol_code_chunk[start_index:].strip()
    print("sub_chunks_dict "+str(sub_chunks_dict))
    return sub_chunks_dict


# .
# *
#  100-INITIALIZE.

# split everything with dots


def parse_cobol_structure(cobol_code_chunk):
    division_pattern = re.compile(r'\b\w+\s+DIVISION\b.*?\.\s*')

    # fix this case COMPUTE LK-RESULT = LK-NUMBER1 * LK-NUMBER2.
    # # Regex pattern
    # pattern = r'\.\n\*.*\n\w*-*\.'
    # # Perform the match
    # matches = re.findall(pattern, sample_string)
    # pattern = r'\.\n\*.*\n\w*-*\.'
    # pattern = r'\.\n/.*\n\w*-*\.'
    # paragraph_pattern = re.compile(r"\.[\s\n]+/.*[\s\n]+(\w*-*)\.")


    pattern_extraction_helper = re.compile(r"\w+(?:-\w+)*\.")
    # pattern_extraction_helper = re.compile(r"\w*(-\w*)*\.")

    # paragraph_pattern1 = re.compile(r"/.*\n\w*-*\.")
    # paragraph_pattern2 = re.compile(r"/.*\n\w*-*\.")

    # paragraph_pattern1 = re.compile(r"\*.*\n\w*-*\.")
    # paragraph_pattern2 = re.compile(r"/.*\n\w*-*\.")

    # paragraph_pattern1 = re.compile(r"\*.*?\n\d+-\w+\.")
    # paragraph_pattern1 = re.compile(r"(\*+|-+)(?:\w+\s*)*[\n]+(\w+(?:-\w+)*)\.")
    # paragraph_pattern1 = re.compile(r"^\s*\*\s*\n\s*(\d+-\w+\.)\s*$")


    paragraph_pattern1 = re.compile(r"^\s*\*.*[\n]\s*(\w+(?:-\w+)*\.\s*)$", re.MULTILINE)
    paragraph_pattern2 = re.compile(r"^\s*/.*[\n]\s*(\w+(?:-\w+)*\.\s*)$", re.MULTILINE)




    # paragraph_pattern1 = re.compile(r"\.\s*\n\*.*\n\w*-*\.")
    # paragraph_pattern2 = re.compile(r"\.\s*\n/.*\n\w*-*\.")
    paragraph_pattern = re.compile(r"(?:\.+|>+|\*?>+|-+)[\s\n]+(\w+(?:-\w+)*)\.")

    # paragraph_pattern = re.compile(r"^\s*\*\s*$(?:\n\s*(\d+-\w+\.\s*))")

    # paragraph_pattern = re.compile(r"(?:\.+|\*+|>+|\*?>+|/+|-+)[\s\n]+(\w+(?:-\w+)*)\.")
    # paragraph_pattern = re.compile(r"(?:\.+|\*+|>+|\*?>+|/+|-+)[\s\n]+(\w+(?:-\w+)?)\.")

    section_pattern = re.compile(r'\b[\w-]+\s+SECTION\.\s*')

    matched_strings_divisions = extract_matching_regex(division_pattern, cobol_code_chunk)
    extracted_divisions = split_on_matched_strings(matched_strings_divisions, cobol_code_chunk)

    extractions = dict()
    for extracted_division_name, extracted_division_content in extracted_divisions.items():

        print("extracted_division_name "+str(extracted_division_name))

        extracted_paragraphs = dict()
        extracted_sections = dict()

        matched_strings_sections = extract_matching_regex(section_pattern, extracted_division_content)
        print("matched_strings_sections "+str(matched_strings_sections))
        extracted_sections = split_on_matched_strings(matched_strings_sections, extracted_division_content)

        if "PROCEDURE DIVISION" in extracted_division_name:
          print("PROCEDURE DIVISION recognized ")
          # print("extracted_division_content "+extracted_division_content)
          # print("not_defined "+str(extracted_sections['not_defined']))
          # print("extracted_sections "+str(extracted_sections))
          # procedure_name  = extracted_sections['not_defined'].split(".")[0]+"."
          # extracted_sections[procedure_name] = extracted_sections.pop('not_defined')

          # matched_strings_paragraphs = extract_matching_regex(paragraph_pattern, extracted_sections['not_defined'])
          # print("matched_strings_paragraphs "+str(matched_strings_paragraphs))
          # matched_strings_paragraphs = [matched_string[1:].strip() for matched_string in matched_strings_paragraphs if matched_string]
          # print("matched_strings_paragraphs "+str(matched_strings_paragraphs))
          # extracted_paragraphs = split_on_metched_strings(matched_strings_paragraphs, extracted_sections['not_defined'])
          # print("extracted_paragraphs "+str(extracted_paragraphs))

          for extracted_section_name, extracted_section_content in extracted_sections.items():
                matched_strings_paragraphs = extract_matching_regex(paragraph_pattern, extracted_section_content)
                # matched_strings_paragraphs = [matched_string[1:].strip() for matched_string in matched_strings_paragraphs if matched_string]


                # print("extracted_section_content "+str(extracted_section_content))

                matched_strings_paragraphs1 = extract_matching_regex(paragraph_pattern1, extracted_section_content)
                print("matched_strings_paragraphs1 "+str(matched_strings_paragraphs1))
                matched_strings_paragraphs2 = extract_matching_regex(paragraph_pattern2, extracted_section_content)
                print("matched_strings_paragraphs2 "+str(matched_strings_paragraphs2))

                if not matched_strings_paragraphs1:
                    break;

                matched_strings_paragraphs.extend(matched_strings_paragraphs1)
                matched_strings_paragraphs.extend(matched_strings_paragraphs2)

                # matched_strings_paragraphs = [
                #     item
                #     for matched_string in matched_strings_paragraphs if matched_string
                #     for item in extract_matching_regex(pattern_extraction_helper, matched_string)
                # ]

                print("matched_strings_paragraphs "+str(matched_strings_paragraphs))
                extracted_section_paragraphs = split_on_matched_strings(matched_strings_paragraphs, extracted_section_content)

                extracted_section_paragraphs_new = dict()
                for extracted_paragraphs_name, extracted_paragraphs_content in extracted_section_paragraphs.items():
                  extracted_paragraphs_name_matched = extract_matching_regex(pattern_extraction_helper, extracted_paragraphs_name)
                  print("extracted_paragraphs_name "+str(extracted_paragraphs_name))
                  print("extracted_paragraphs_name_matched "+str(extracted_paragraphs_name_matched))
                  if extracted_paragraphs_name_matched:
                    extracted_paragraphs_name_new = extracted_paragraphs_name_matched[0]
                  else:
                    extracted_paragraphs_name_new = extracted_paragraphs_name
                  extracted_section_paragraphs_new[extracted_paragraphs_name_new] = extracted_paragraphs_content


                # print("extracted_section_content "+str(extracted_section_content))
                # print("extracted_section_paragraphs "+str(extracted_section_paragraphs))
                extracted_sections[extracted_section_name] = {"extracted_section_content":extracted_section_content,
                                                              "extracted_section_paragraphs":extracted_section_paragraphs_new}

        # print("extracted_sections "+str(extracted_sections))
        # print("extracted_paragraphs "+str(extracted_paragraphs))
        # print("extracted_division_name "+str(extracted_division_name))

        extractions[extracted_division_name] = {"sections":dict(),"paragraphs":dict()}
        extractions[extracted_division_name]["sections"].update(extracted_sections)
        extractions[extracted_division_name]["paragraphs"].update(extracted_paragraphs)

    return extractions


def parse_cobol_to_json(cobol_code_chunk):
    parsed_dict = parse_cobol_structure(cobol_code_chunk)
    json_string = json.dumps(parsed_dict)
    return json_string