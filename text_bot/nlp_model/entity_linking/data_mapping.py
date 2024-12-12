import pandas as pd
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from difflib import SequenceMatcher
import math


def get_value_from_record(record, key):
    """
    Retrieves the value for a given key from the record,
    considering possible suffixes like '-2', '-3', etc.
    """
    for k, v in record.items():
        if k == key or k.startswith(f"{key}-"):
            return v
    return None

def extract_dnb_individual_fields(record):
    """
    Extracts relevant fields from a DnB individual record for matching.
    """
    dnb_fields = {}
    dnb_fields['given_name'] = get_value_from_record(record, 'given_name') or ''
    dnb_fields['middle_name'] = get_value_from_record(record, 'middle_name') or ''
    dnb_fields['family_name'] = get_value_from_record(record, 'family_name') or get_value_from_record(record, 'last_name') or ''
    dnb_fields['full_name'] = get_value_from_record(record, 'full_name') or ''
    dnb_fields['prefix_name'] = get_value_from_record(record, 'prefix_name') or ''
    dnb_fields['suffix_name'] = get_value_from_record(record, 'suffix_name') or ''
    dnb_fields['gender'] = get_value_from_record(record, 'gender') or ''
    dnb_fields['birth_date'] = get_value_from_record(record, 'birth_date') or ''
    dnb_fields['nationality'] = get_value_from_record(record, 'nationality') or ''
    dnb_fields['residence_country'] = get_value_from_record(record, 'residence_country') or ''
    return dnb_fields


def extract_dj_acuris_individual_fields(record):
    """
    Extracts relevant fields from a DJ Acuris individual record for matching.
    """
    dj_fields = {}
    dj_fields['matched_name'] = get_value_from_record(record, 'matched_name') or ''
    dj_fields['first_name'] = get_value_from_record(record, 'first_name') or ''
    dj_fields['middle_name'] = get_value_from_record(record, 'middle_name') or ''
    dj_fields['surname'] = get_value_from_record(record, 'surname') or get_value_from_record(record, 'last_name') or ''
    dj_fields['screened_name'] = get_value_from_record(record, 'screened_name') or ''
    dj_fields['title'] = get_value_from_record(record, 'title') or ''
    dj_fields['gender'] = get_value_from_record(record, 'gender') or ''
    dj_fields['dates_of_birth'] = []
    dj_fields['citizenship'] = []
    dj_fields['residence'] = []

    # Parse 'description_json' if present
    description_json_str = get_value_from_record(record, 'description_json')
    if description_json_str and isinstance(description_json_str, str):
        try:
            description_data = json.loads(description_json_str)
            # Extract fields from description_data as needed
            dj_fields['dates_of_birth'] = description_data.get('dates_of_birth', dj_fields['dates_of_birth'])
            citizenship = description_data.get('citizenship')
            if citizenship:
                dj_fields['citizenship'] = [citizenship] if isinstance(citizenship, str) else citizenship
            residency = description_data.get('residency')
            if residency:
                dj_fields['residence'] = [residency] if isinstance(residency, str) else residency
            dj_fields['gender'] = description_data.get('gender', dj_fields['gender'])
        except json.JSONDecodeError:
            pass  # Handle or log error if needed
    return dj_fields


def extract_dnb_and_dj_acuris_lists(csv_prepared_json_list):
    # Initialize lists to hold the extracted individual data
    dnb_individuals = []
    dj_individuals = []
    for record in csv_prepared_json_list:

        dnb_individual = extract_dnb_individual_fields(record)
        dnb_individuals.append(dnb_individual)

        dj_individual = extract_dj_acuris_individual_fields(record)
        dj_individuals.append(dj_individual)

    return dnb_individuals, dj_individuals



def compare_individuals(dnb_individuals, dj_individuals):
    matches = []
    for dnb_person in dnb_individuals:
        dnb_full_name = ' '.join(filter(None, [
            dnb_person.get('given_name', ''),
            dnb_person.get('middle_name', ''),
            dnb_person.get('family_name', '')
        ])).strip().lower()
        dnb_birth_date = dnb_person.get('birth_date', '')
        dnb_nationality = dnb_person.get('nationality', '').lower()
        dnb_residence = dnb_person.get('residence_country', '').lower()
        dnb_gender = dnb_person.get('gender', '').lower()

        for dj_person in dj_individuals:
            dj_full_name = ' '.join(filter(None, [
                dj_person.get('first_name', ''),
                dj_person.get('middle_name', ''),
                dj_person.get('surname', '')
            ])).strip().lower()
            dj_birth_dates = dj_person.get('dates_of_birth', [])
            dj_citizenships = [c.lower() for c in dj_person.get('citizenship', [])]
            dj_residences = [r.lower() for r in dj_person.get('residence', [])]
            dj_gender = dj_person.get('gender', '').lower()

            # Compare names
            name_similarity = SequenceMatcher(None, dnb_full_name, dj_full_name).ratio()
            if name_similarity > 0.8:
                # Further comparisons (date of birth, nationality, etc.)
                dob_match = any(dnb_birth_date == dj_dob for dj_dob in dj_birth_dates)
                nationality_match = dnb_nationality in dj_citizenships
                residence_match = dnb_residence in dj_residences
                gender_match = dnb_gender == dj_gender and dnb_gender != ''

                # Collect match information
                match_info = {
                    'dnb_person': dnb_person,
                    'dj_person': dj_person,
                    'name_similarity': name_similarity,
                    'dob_match': dob_match,
                    'nationality_match': nationality_match,
                    'residence_match': residence_match,
                    'gender_match': gender_match
                }
                matches.append(match_info)
    return matches

def compare_dnb_person_to_dj(dnb_person, dj_individuals):
    matches = []

    dnb_full_name = ' '.join(filter(None, [
        dnb_person.get('given_name', ''),
        dnb_person.get('middle_name', ''),
        dnb_person.get('family_name', '')
    ])).strip().lower()
    dnb_birth_date = dnb_person.get('birth_date', '')
    dnb_nationality = dnb_person.get('nationality', '').lower()
    dnb_residence = dnb_person.get('residence_country', '').lower()
    dnb_gender = dnb_person.get('gender', '').lower()

    for dj_person in dj_individuals:
        dj_full_name = ' '.join(filter(None, [
            dj_person.get('first_name', ''),
            dj_person.get('middle_name', ''),
            dj_person.get('surname', '')
        ])).strip().lower()
        dj_birth_dates = dj_person.get('dates_of_birth', [])
        dj_citizenships = [c.lower() for c in dj_person.get('citizenship', [])]
        dj_residences = [r.lower() for r in dj_person.get('residence', [])]
        dj_gender = dj_person.get('gender', '').lower()

        # Compare names
        name_similarity = SequenceMatcher(None, dnb_full_name, dj_full_name).ratio()
        if name_similarity > 0.8:
            # Further comparisons (date of birth, nationality, etc.)
            dob_match = any(dnb_birth_date == dj_dob for dj_dob in dj_birth_dates)
            nationality_match = dnb_nationality in dj_citizenships
            residence_match = dnb_residence in dj_residences
            gender_match = dnb_gender == dj_gender and dnb_gender != ''

            # # Collect match information
            # match_info = {
            #     'dnb_person': dnb_person,
            #     'dj_person': dj_person,
            #     'name_similarity': name_similarity,
            #     'dob_match': dob_match,
            #     'nationality_match': nationality_match,
            #     'residence_match': residence_match,
            #     'gender_match': gender_match
            # }
            matches.append(dj_person)
    return matches



def compare_persons(dnb_data_list, dj_acuris_data_list, threshold=0.8):
    """
    Compare DnB data with Dow Jones/Acuris data to find possibly associated persons.

    Parameters:
    - dnb_data_list: List of dictionaries containing DnB person data.
    - dj_acuris_data_list: List of dictionaries containing DJ/Acuris person data.
    - threshold: A float between 0 and 1 representing the minimum match score to consider a match.

    Returns:
    - matches: A list of dictionaries containing matching person pairs and their match scores.
    """


    matches = []

    # Weights for each field
    weights = {
        'name': 0.5,
        'date_of_birth': 0.2,
        'nationality': 0.15,
        'residence_country': 0.1,
        'gender': 0.05
    }

    for dnb_person in dnb_data_list:
        # Construct the full name for the DnB person
        dnb_full_name = ' '.join(filter(None, [
            dnb_person.get('given_name', ''),
            dnb_person.get('middle_name', ''),
            dnb_person.get('family_name', ''),
            dnb_person.get('suffix_name', '')
        ])).strip().lower()

        dnb_dob = dnb_person.get('birth_date', '')
        dnb_nationality = dnb_person.get('nationality', '').lower()
        dnb_residence = dnb_person.get('residence_country', '').lower()
        dnb_gender = dnb_person.get('gender', '').lower()

        for dj_person in dj_acuris_data_list:
            # Construct the full name for the DJ/Acuris person
            dj_full_name = ' '.join(filter(None, [
                dj_person.get('first_name', ''),
                dj_person.get('middle_name', ''),
                dj_person.get('surname', ''),
                dj_person.get('suffix_name', '')
            ])).strip().lower()

            # If 'dates_of_birth' is a list, consider all possible dates
            dj_dobs = dj_person.get('dates_of_birth', [])
            dj_nationalities = dj_person.get('citizenship', []) or dj_person.get('nationality', [])
            dj_residences = dj_person.get('residence', []) or dj_person.get('residence_country', [])
            dj_gender = dj_person.get('gender', '').lower()

            # Initialize match score
            match_score = 0.0

            # Name similarity
            name_similarity = SequenceMatcher(None, dnb_full_name, dj_full_name).ratio()
            match_score += weights['name'] * name_similarity

            # Date of birth match
            dob_match = 0.0
            for dj_dob in dj_dobs:
                if dnb_dob and dj_dob:
                    if dnb_dob == dj_dob:
                        dob_match = 1.0
                        break
                    elif dnb_dob[:7] == dj_dob[:7]:  # Match up to month
                        dob_match = 0.8
                    elif dnb_dob[:4] == dj_dob[:4]:  # Match up to year
                        dob_match = 0.5
            match_score += weights['date_of_birth'] * dob_match

            # Nationality match
            nationality_match = 0.0
            for dj_nat in dj_nationalities:
                if dnb_nationality and dj_nat.lower() == dnb_nationality:
                    nationality_match = 1.0
                    break
            match_score += weights['nationality'] * nationality_match

            # Residence country match
            residence_match = 0.0
            for dj_res in dj_residences:
                if dnb_residence and dj_res.lower() == dnb_residence:
                    residence_match = 1.0
                    break
            match_score += weights['residence_country'] * residence_match

            # Gender match
            gender_match = 1.0 if dnb_gender == dj_gender and dnb_gender else 0.0
            match_score += weights['gender'] * gender_match

            # Check if match score meets the threshold
            if match_score >= threshold:
                match_info = {
                    'dnb_person': dnb_person,
                    'dj_person': dj_person,
                    'match_score': match_score,
                    'details': {
                        'name_similarity': name_similarity,
                        'dob_match': dob_match,
                        'nationality_match': nationality_match,
                        'residence_match': residence_match,
                        'gender_match': gender_match
                    }
                }
                matches.append(match_info)

    return matches

def safe_str(value):
    """Convert the value to a string if possible; otherwise, return an empty string."""
    if isinstance(value, str):
        return value
    elif value is None or (isinstance(value, float) and math.isnan(value)):
        return ''
    else:
        return str(value)

def find_dnb_match_in_dj_acuris(dnb_person, dj_acuris_data_list, threshold=0.5):
    """
    Compare DnB data with Dow Jones/Acuris data to find possibly associated persons.

    Parameters:
    - dnb_data_list: List of dictionaries containing DnB person data.
    - dj_acuris_data_list: List of dictionaries containing DJ/Acuris person data.
    - threshold: A float between 0 and 1 representing the minimum match score to consider a match.

    Returns:
    - matches: A list of dictionaries containing matching person pairs and their match scores.
    """


    matches = []

    # Weights for each field
    weights = {
        'name': 0.5,
        'date_of_birth': 0.2,
        'nationality': 0.15,
        'residence_country': 0.1,
        'gender': 0.05
    }

    # Construct the full name for the DnB person
    dnb_full_name = ' '.join(filter(None, [
        safe_str(dnb_person.get('given_name', '')),
        safe_str(dnb_person.get('middle_name', '')),
        safe_str(dnb_person.get('family_name', '')),
        safe_str(dnb_person.get('suffix_name', ''))
    ])).strip().lower()

    dnb_dob = safe_str(dnb_person.get('birth_date', ''))
    dnb_nationality = safe_str(dnb_person.get('nationality', '')).lower()
    dnb_residence = safe_str(dnb_person.get('residence_country', '')).lower()
    dnb_gender = safe_str(dnb_person.get('gender', '')).lower()

    for dj_person in dj_acuris_data_list:
        # Construct the full name for the DJ/Acuris person
        dj_full_name = ' '.join(filter(None, [
            safe_str(dj_person.get('first_name', '')),
            safe_str(dj_person.get('middle_name', '')),
            safe_str(dj_person.get('surname', '')),
            safe_str(dj_person.get('suffix_name', ''))
        ])).strip().lower()

        # Ensure gender is a string
        dj_gender = safe_str(dj_person.get('gender', '')).lower()

        # Process dates_of_birth, citizenship, and residence if they are lists
        dj_dobs = [safe_str(dob) for dob in dj_person.get('dates_of_birth', [])]
        dj_nationalities = [safe_str(nat).lower() for nat in dj_person.get('citizenship', [])+[safe_str(dj_person.get('nationality', ""))]]
        dj_residences = [safe_str(res).lower() for res in
                         dj_person.get('residence', [])+[safe_str(dj_person.get('residence_country', ""))]]


        # Initialize match score
        match_score = 0.0

        # Name similarity
        name_similarity = SequenceMatcher(None, dnb_full_name, dj_full_name).ratio()
        match_score += weights['name'] * name_similarity

        # Date of birth match
        dob_match = 0.0
        for dj_dob in dj_dobs:
            if dnb_dob and dj_dob:
                if dnb_dob == dj_dob:
                    dob_match = 1.0
                    break
                elif dnb_dob[:7] == dj_dob[:7]:  # Match up to month
                    dob_match = 0.8
                elif dnb_dob[:4] == dj_dob[:4]:  # Match up to year
                    dob_match = 0.5
        match_score += weights['date_of_birth'] * dob_match

        # Nationality match
        nationality_match = 0.0
        for dj_nat in dj_nationalities:
            if dnb_nationality and dj_nat.lower() == dnb_nationality:
                nationality_match = 1.0
                break
        match_score += weights['nationality'] * nationality_match

        # Residence country match
        residence_match = 0.0
        for dj_res in dj_residences:
            if dnb_residence and dj_res.lower() == dnb_residence:
                residence_match = 1.0
                break
        match_score += weights['residence_country'] * residence_match

        # Gender match
        gender_match = 1.0 if dnb_gender == dj_gender and dnb_gender else 0.0
        match_score += weights['gender'] * gender_match

        # Check if match score meets the threshold
        if match_score >= threshold:
            match_info = {
                'dnb_person': dnb_person,
                'dj_person': dj_person,
                'match_score': match_score,
                'details': {
                    'name_similarity': name_similarity,
                    'dob_match': dob_match,
                    'nationality_match': nationality_match,
                    'residence_match': residence_match,
                    'gender_match': gender_match
                }
            }
            matches.append(match_info)

    return matches



def extract_dnb_fields(row: pd.Series) -> Dict[str, Any]:
    """
    Extract important fields from a DnB data row and return a dictionary.
    """
    dnb_data = {}

    # Extract basic individual details
    dnb_data['given_name'] = row.get('given_name', '')
    dnb_data['middle_name'] = row.get('middle_name', '')
    dnb_data['family_name'] = row.get('family_name', '')
    dnb_data['full_name'] = row.get('full_name', '')
    dnb_data['prefix_name'] = row.get('prefix_name', '')
    dnb_data['suffix_name'] = row.get('suffix_name', '')
    dnb_data['gender'] = row.get('gender', '')
    dnb_data['birth_date'] = row.get('birth_date', '')
    dnb_data['nationality'] = row.get('nationality', '')
    dnb_data['residence_country'] = row.get('residence_country', '')

    # Extract company details if applicable
    dnb_data['duns'] = row.get('duns', '')
    dnb_data['company_name'] = row.get('name', '')
    dnb_data['country_code'] = row.get('country_code', '')
    dnb_data['address'] = {
        'address_line1': row.get('address_line1', ''),
        'address_line2': row.get('address_line2', ''),
        'address_line3': row.get('address_line3', ''),
        'address_line4': row.get('address_line4', ''),
        'post_code': row.get('post_code', ''),
        'city': row.get('city', ''),
        'state_province': row.get('state_province', '')
    }
    dnb_data['phone'] = row.get('phone', '')
    dnb_data['fax'] = row.get('fax', '')
    dnb_data['website'] = row.get('website', '')
    dnb_data['number_of_employees'] = row.get('number_of_employees', '')

    # Parse any JSON fields if present
    business_entity_type_json = row.get('business_entity_type', '{}')
    try:
        dnb_data['business_entity_type'] = json.loads(business_entity_type_json)
    except json.JSONDecodeError:
        dnb_data['business_entity_type'] = {}

    registration_numbers_json = row.get('registration_numbers', '[]')
    try:
        dnb_data['registration_numbers'] = json.loads(registration_numbers_json)
    except json.JSONDecodeError:
        dnb_data['registration_numbers'] = []

    # Add any other important fields as needed

    return dnb_data


def extract_dj_acuris_fields(row: pd.Series) -> Dict[str, Any]:
    """
    Extract important fields from a Dow Jones/Acuris data row and return a dictionary.
    """
    dj_data = {}

    # Extract basic individual details
    dj_data['matched_name'] = row.get('matched_name', '')
    dj_data['primary_name'] = row.get('primary_name', '')
    dj_data['screened_name'] = row.get('screened_name', '')
    dj_data['title'] = row.get('title', '')
    dj_data['gender'] = row.get('gender', '')
    dj_data['date_of_birth'] = row.get('date_of_birth', '')
    dj_data['nationality'] = row.get('nationality', '')
    dj_data['residence_country'] = row.get('residence_country', '')
    dj_data['citizenship'] = row.get('citizen', '')

    # Extract compliance indicators
    dj_data['is_pep'] = row.get('is_pep', '')
    dj_data['is_sanctioned'] = row.get('is_sanctioned', '')
    dj_data['has_adverse_media'] = row.get('has_adverse_media', '')
    dj_data['risk'] = row.get('risk', '')
    dj_data['status'] = row.get('status', '')

    # Extract scores
    dj_data['score'] = row.get('score', '')
    dj_data['score_pep'] = row.get('score_pep', '')
    dj_data['score_sanction'] = row.get('score_sanction', '')
    dj_data['score_adverse_media'] = row.get('score_adverse_media', '')
    dj_data['matching_score'] = row.get('matching_score', '')

    # Parse JSON fields
    description_json_str = row.get('description_json', '{}')
    try:
        description_json = json.loads(description_json_str)
        # Extract relevant fields from description_json
        attributes = description_json.get('data', {}).get('attributes', {})

        # Names
        name_details = attributes.get('basic', {}).get('name_details', {})
        primary_name = name_details.get('primary_name', {})

        dj_data['first_name'] = primary_name.get('first_name', '')
        dj_data['middle_name'] = primary_name.get('middle_name', '')
        dj_data['surname'] = primary_name.get('surname', '')

        # Dates of birth
        date_details = attributes.get('person', {}).get('date_details', {})
        birth_dates = date_details.get('birth', [])
        dob_list = []
        for dob in birth_dates:
            date = dob.get('date', {})
            year = date.get('year')
            month = date.get('month')
            day = date.get('day')
            dob_formatted = f"{year}-{month or '01'}-{day or '01'}"
            dob_list.append(dob_formatted)
        dj_data['dates_of_birth'] = dob_list

        # Nationality and residence
        country_details = attributes.get('person', {}).get('country_territory_details', {})
        citizenship = country_details.get('citizenship', [])
        residence = country_details.get('residence', [])
        dj_data['citizenship'] = [c.get('descriptor', '') for c in citizenship]
        dj_data['residence'] = [r.get('descriptor', '') for r in residence]

        # Gender
        dj_data['gender'] = attributes.get('person', {}).get('gender', '')

        # Risk indicators
        dj_data['icon_hints'] = attributes.get('person', {}).get('icon_hints', [])

    except json.JSONDecodeError:
        # Handle JSON parsing errors
        pass

    # Parse XML fields if necessary
    # For example, parsing 'description_xml' or 'short_description_xml'
    # Implement XML parsing similar to JSON parsing if needed

    # Add any other important fields as needed

    return dj_data
