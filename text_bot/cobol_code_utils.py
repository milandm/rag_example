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

    current_division = None
    current_section = None
    section_content = []

    for line in cobol_code.splitlines():
        line = line.strip()

        # Check for a new division
        division_match = re.match(r'(IDENTIFICATION|ENVIRONMENT|DATA|PROCEDURE) DIVISION\.', line)
        if division_match:
            # Save the previous section content
            if current_section and section_content:
                divisions[current_division][current_section] = "\n".join(section_content)
                section_content = []

            current_division = division_match.group()
            current_section = None
            continue

        # Check for a new section
        section_match = re.match(r'(\w+ SECTION)\.', line)
        if section_match and current_division in divisions:
            # Save the previous section content
            if current_section and section_content:
                divisions[current_division][current_section] = "\n".join(section_content)
                section_content = []

            current_section = section_match.group(1)
            continue

        # If we're in a section, accumulate the lines
        if current_section is not None:
            section_content.append(line)

    # Save the last section's content
    if current_section and section_content:
        divisions[current_division][current_section] = "\n".join(section_content)

    # Convert the divisions dictionary to JSON
    json_output = json.dumps(divisions, indent=4)
    return json_output
