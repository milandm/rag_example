import spacy
import re
from datetime import datetime
import pytesseract
from PIL import Image
import json
from spacy_langdetect import LanguageDetector
from spacy.language import Language


# Add the language detector to the pipeline
@Language.factory("language_detector")
def get_lang_detector(nlp, name):
    return LanguageDetector()

def get_langugage(text):
    # Load a SpaCy model
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('language_detector', last=True)

    doc = nlp(text)
    return  doc._.language['language']




extracted_info = {
    'certification_authority': None,
    'certificate_type': None,
    'certification_date': None,
    'valid_from': None,
    'valid_to': None,
    'company_name': None,
    'address': None,
    'activity_material_group': None
}


def load_model_by_language(language_code):
    if language_code == 'en':
        return spacy.load('en_core_web_sm')
    elif language_code == 'fr':
        return spacy.load('fr_core_news_sm')
    elif language_code == 'de':
        return spacy.load('de_core_news_sm')
    elif language_code == 'es':
        return spacy.load('es_core_news_sm')
    elif language_code == 'pt':
        return spacy.load('pt_core_news_sm')
    # Add more languages as needed
    else:
        raise ValueError(f"No model available for language code: {language_code}")



def extract_information(language_code, text):

    try:
        nlp = load_model_by_language(language_code)
        # Process the text with the correct model
        doc = nlp(text)
        print(f"Processed text with {language_code} model")
    except ValueError as e:
        print(e)


    # Extract entities using NER
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            extracted_info['certification_authority'] = ent.text
        elif ent.label_ == 'DATE':
            date = re.search(r'\d{1,2}\s\w+\s\d{4}', ent.text)
            if date:
                extracted_date = datetime.strptime(date.group(), '%d %B %Y')
                if extracted_info['certification_date'] is None or extracted_date < extracted_info[
                    'certification_date']:
                    extracted_info['certification_date'] = extracted_date
                elif extracted_info['valid_from'] is None or extracted_date < extracted_info['valid_from']:
                    extracted_info['valid_from'] = extracted_date
                elif extracted_info['valid_to'] is None or extracted_date > extracted_info['valid_to']:
                    extracted_info['valid_to'] = extracted_date
        elif ent.label_ == 'GPE':
            extracted_info['address'] = ent.text
        elif ent.label_ == 'PERSON':
            extracted_info['company_name'] = ent.text

    # Extract specific fields using regular expressions
    cert_type = re.search(r'ISO\s\d{4,5}(:\d{4})?', text)
    if cert_type:
        extracted_info['certificate_type'] = cert_type.group()

    # activity = re.search(r'activity\s*:\s*(.*)', text, re.IGNORECASE)
    # if activity:
    #     extracted_info['activity_material_group'] = activity.group(1).strip()

    return extracted_info


# print(json.dumps(info, indent=4, default=str))