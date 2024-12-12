from custom_logger.universal_logger import UniversalLogger
from rapidfuzz import process as rapidfuzzProcess
from fuzzywuzzy import process as fuzzywuzzyProcess
from pydantic import BaseModel


CERTIFICATE_TYPES = {
    "9001":"ISO 9001",
    "14001":"ISO 14001",
    "50001":"ISO 50001",
    "45001":"ISO 45001"}


companies_names_list  = ['Saint-Gobain Performance Plastics (Shanghai) Co., Ltd.', 'Freudenberg FST GmbH', 'SAINT-GOBAIN PERFORMANCE PLASTICS FRANCE', 'Saint-Gobain Performance Plastics', 'MELEXIS Technologies NV', 'Saint-Gobain Performance Plastics Korea Co., Ltd.', 'Saint-Gobain Performance Plastics Corporation', 'ALLADA SGPP FRANCE (GROUPE SAINT-GOBAIN)', 'Saint-Gobain Performance Plastics (Shanghai) Co., Ltd.', 'OLYMPIC BROADCASTING SERVICES, S.L.', 'Freudenberg Joints Plats S.A.S. FST Gaskets Devision', 'SAS GYS', 'Saint-Gobain Performance Plastics', 'Iron Mountain Records Management (Shanghai) Co., Ltd.', 'Freudenberg Sealing Technologies San. ve Tic. Anonim Şirketi', 'SAINT-GOBAIN PERFORMANCE PLASTICS FRANCE', 'SGS Saint Gobain Performance Plastics', 'Freudenberg-NOK Sealing Technologies Freudenberg-NOK General Partnership', 'Freudenberg Sealing Technologies Sanayi ve Ticaret A.S.', 'SGPP FRANCE (GROUPE SAINT-GOBAIN)', 'Saint-Gobain Performance Plastics L+S GmbH', 'Saint-Gobain Performance Plastics', 'SAINT-GOBAIN PERFORMANCE PLASTICS FRANCE', 'Freudenberg Sealing Technologies S.a.s. di Externa Italia S.r.l.u.', 'Melexis NV', 'Saint-Gobain Performance Plastics', 'Freudenberg Sealing Technologies Ltd', 'Freudenberg FST GmbH', 'Freudenberg-NOK Sealing Technologies Freudenberg-NOK General Partnership', 'SERVA Electrophoresis GmbH', 'Saint-Gobain Performance Plastics Isofluor GmbH', 'SAINT-GOBAIN PERFORMANCE PLASTICS CORPORATION', 'SANT GOBAIN PERFORMANCE PLASTICS (HANGZHOU) CO., LTD.', 'Changchun Integral Accumulator Co. Ltd.', 'Human Settlements Adjudication Commission', 'Melexis Bulgaria Ltd.', 'Freudenberg Sealing Technologies Kft.', 'Freudenberg FST GmbH', 'Melexis Bulgaria Ltd.', 'Freudenberg Sealing Technologies Kft.', 'Melexis', 'SERVA Electrophoresis GmbH', 'Melexis NV', 'Melexis NV', 'Saint-Gobain Performance Plastics Korea', 'Saint-Gobain Performance Plastics', 'Freudenberg-NOK Sealing Technologies Freudenberg-NOK General Partnership', 'Saint-Gobain Performance Plastics', 'MS Techniques SAS', 'Saint-Gobain Life Sciences Ireland', 'Freudenberg-NOK Sealing Technologies Freudenberg-NOK General Partnership', 'SAINT-GOBAIN PERFORMANCE PLASTICS FRANCE', 'Saint-Gobain Life Sciences (Hangzhou) Co., Ltd.', 'Grindwell Norton Limited', 'Equflow B.V.', 'SAINT-GOBAIN PERFORMANCE PLASTICS FRANCE', 'SIVA SIVANI DEGREE COLLEGE', 'Saint-Gobain Performance Plastics Corporation', 'Freudenberg-NOK Sealing Technologies Freudenberg-NOK General Partnership', 'Freudenberg Sealing Technologies Sp.zo.o.', 'FREUDENBERG-NOK PRIVATE LIMITED', 'SAINT-GOBAIN PERFORMANCE PLASTICS CORPORATION', 'Saint-Gobain Performance Plastics', 'Saint-Gobain Performance Plastics L + S GmbH', 'Saint-Gobain Performance Plastics', 'SAINT-GOBAIN K.K. PERFORMANCE PLASTICS', 'Melexis Bulgaria Ltd.', 'Saint-Gobain Performance Plastics Korea Co., Ltd.', 'VITLAB GmbH', 'AGLIARE SGPP FRANCE (GROUPE SAINT-GOBAIN)', 'Freudenberg FST GmbH', 'Bureau Veritas', 'Freudenberg Joints Plats S.A.S. FST Gaskets Devision', 'Melexis NV', 'TRANSLUMINAL', 'Melexis NV', 'Saint-Gobain Performance Plastics (Shanghai) Co., Ltd.', 'Transluminal SARL', 'Saint-Gobain Performance Plastics Isofluor GmbH', 'Melexis NV', 'Freudenberg-NOK Sealing Technologies Freudenberg-NOK General Partnership', 'Lederer GmbH', 'Saint-Gobain Performance Plastics L+S GmbH', 'Saint Gobain Performance Plastics', 'SGPP FRANCE (GROUPE SAINT-GOBAIN)', 'SAINT-GOBAIN Performance Plastics (Shanghai) Co., Ltd.', 'SAINT GOBAIN PERFORMANCE PLASTICS FRANCE', 'GRINDWELL NORTON LIMITED', 'SAINT-GOBAIN DO BRASIL PRODUTOS INDUSTRIAIS E PARA CONSTRUCAO LTDA', 'Saint-Gobain Performance Plastics', 'Saint-Gobain Performance Plastics', 'Saint Gobain Performance Plastics', 'Freudenberg-NOK Private Limited']

unique_companies_names_list = [
    'Saint-Gobain Performance Plastics (Shanghai) Co.,'' Ltd.',
    'Freudenberg FST GmbH',
    'SAINT-GOBAIN PERFORMANCE PLASTICS FRANCE',
    'Saint-Gobain Performance Plastics',
    'MELEXIS Technologies NV',
    'Saint-Gobain Performance Plastics Korea Co., Ltd.',
    'Saint-Gobain Performance Plastics Corporation',
    'ALLADA SGPP FRANCE (GROUPE SAINT-GOBAIN)',
    'OLYMPIC BROADCASTING SERVICES, S.L.',
    'Freudenberg Joints Plats S.A.S. FST Gaskets Devision',
    'SAS GYS',
    'Iron Mountain Records Management (Shanghai) Co., Ltd.',
    'Freudenberg Sealing Technologies San. ve Tic. Anonim Şirketi',
    'SGS Saint Gobain Performance Plastics',
    'Freudenberg-NOK Sealing Technologies Freudenberg-NOK General Partnership',
    'Freudenberg Sealing Technologies Sanayi ve Ticaret A.S.',
    'SGPP FRANCE (GROUPE SAINT-GOBAIN)',
    'Saint-Gobain Performance Plastics L+S GmbH',
    'Freudenberg Sealing Technologies S.a.s. di Externa Italia S.r.l.u.',
    'Melexis NV',
    'Freudenberg Sealing Technologies Ltd',
    'SERVA Electrophoresis GmbH',
    'Saint-Gobain Performance Plastics Isofluor GmbH',
    'SANT GOBAIN PERFORMANCE PLASTICS (HANGZHOU) CO., LTD.',
    'Changchun Integral Accumulator Co. Ltd.',
    'Human Settlements Adjudication Commission',
    'Melexis Bulgaria Ltd.',
    'Freudenberg Sealing Technologies Kft.',
    'Melexis',
    'Saint-Gobain Performance Plastics Korea',
    'MS Techniques SAS',
    'Saint-Gobain Life Sciences Ireland',
    'Saint-Gobain Life Sciences (Hangzhou) Co., Ltd.',
    'Grindwell Norton Limited',
    'Equflow B.V.',
    'SIVA SIVANI DEGREE COLLEGE',
    'Freudenberg Sealing Technologies Sp.zo.o.',
    'FREUDENBERG-NOK PRIVATE LIMITED',
    'SAINT-GOBAIN K.K. PERFORMANCE PLASTICS',
    'VITLAB GmbH',
    'AGLIARE SGPP FRANCE (GROUPE SAINT-GOBAIN)',
    'Bureau Veritas',
    'Transluminal SARL',
    'Lederer GmbH',
    'Saint Gobain Performance Plastics',
    'GRINDWELL NORTON LIMITED',
    'SAINT-GOBAIN DO BRASIL PRODUTOS INDUSTRIAIS E PARA CONSTRUCAO LTDA',
    'Freudenberg-NOK Private Limited'
]

OFFICIAL_COMPANY_NAMES = [
    "grindwell norton limited",
    "neant",
    "bureau veritas s.a.",
    "nbk keramik gmbh",
    "vitlab gmbh",
    "saint-gobain performance plastics corporation",
    "sgs saint-gobain performance plastics corporation",
    "lederer gmbh",
    "pepperl fuchs",
    "centre technologique alphanov",
    "olympic broadcasting services, s.l.",
    "serva electrophoresis gmbh",
    "schneider electric france",
    "europe qualite france",
    "equflow b.v.",
    "radware ltd.",
    "transluminal sarl",
    "sgs saint gobain performance plastics",
    "ms techniques sas",
    "rader vogel",
    "bmw france",
    "melexis technologies nv",
    "freudenberg sealing technologies gmbh & co. kg",
    "siva sivani degree college",
    "freudenberg sealing technologies kft.",
    "pepperl + fuchs se",
    "d m h france",
    "human settlements adjudication commission",
    "saint-gobain life sciences ireland",
    "grammer ad bulgaria",
    "vadeca facility services, s.a.",
    "saint-gobain life sciences corporation",
    "iron mountain records management co., ltd.",
    "sas gys",
    "grammer ag mg",
    "automotive performance materials",
    "grammer ag",
    "ningbo jiurun",
    "emirates float glass",
    "cerba xpert",
    "miretti s.r.l.",
    "infonet",
    "changchun integral accumulator co., ltd.",
    "new vision"
]

OFFICIAL_COMPANY_NAMES_V1 = [
    'Saint-Gobain Performance Plastics Corporation',
    'Freudenberg Sealing Technologies GmbH & Co. KG',
    'Melexis Technologies NV',
    'Olympic Broadcasting Services, S.L.',
    'SAS GYS',
    'Iron Mountain Records Management Co., Ltd.',
    'SGS Saint-Gobain Performance Plastics Corporation',
    'SERVA Electrophoresis GmbH',
    'Changchun Integral Accumulator Co., Ltd.',
    'Human Settlements Adjudication Commission',
    'MS Techniques SAS',
    'Saint-Gobain Life Sciences Corporation',
    'Grindwell Norton Limited',
    'Equflow B.V.',
    'Siva Sivani Degree College',
    'VITLAB GmbH',
    'Bureau Veritas S.A.',
    'Transluminal SARL',
    'Lederer GmbH',
    'OLYMPIC BROADCASTING SERVICES, S.L.',
    'SGS Saint Gobain Performance Plastics',
    'Saint-Gobain Life Sciences Ireland',
    'Freudenberg Sealing Technologies Kft.',
    'NINGBO JIURUN',
    'RADER VOGEL',
    'GRAMMER AD BULGARIA',
    'GRAMMER AG MG',
    'GRAMMER AG',
    'PEPPERL FUCHS'
]


COMPANY_NAMES = [
    "NINGBO JIUREN MACHINARY CO. LTD",
    "RÄDER-VOGEL - Räder- und Rollenfabrik",
    "GRAMMER AG",
    "PEPPERL+FUCHS AB"]


MATERIAL_GROUPS = [
    "Laser cutting",
    "Stamping",
    "Deep drawn",
    "Turning",
    "Milling",
    "Direct Material",
    "Steel components",
    "Machining",
    "Sheet metal (<15 mm)",
    "Drive wheels Prime",
    "Drive wheels PUR",
    "Drive wheels friction",
    "Drive wheels ESD",
    "Rollers Prime",
    "Rollers PUR",
    "Rollers friction",
    "Support arm wheels Prime",
    "Support arm wheels ESD",
    "Support arm wheels PUR",
    "Wheels", "Drive wheels",
    "Rollers", "Support arm wheels",
    "Miscellaneous", "Seats",
    "Finished products",
    "Seat",
    "Sensors",
    "Electronics",
    "Electronic components",
    "Maintenance and operating of sites",
    "Sites maintenance and operating",
    "Maintenance of buildings",
    "Surveillance, "
    "safety and security",
    "Safety", "Security",
    "Cleaning and desinfecting",
    "Facility management"
]

MATERIAL_GROUP_CODES = {
    "Laser cutting": "501010",
    "Stamping": "501020",
    "Deep drawn": "501030",
    "Turning": "502010",
    "Milling": "502020",
    "Direct Material": "DM",
    "Steel components": "180000",
    "Machining": "180300",
    "Sheet metal (<15 mm)": "180600",
    "Drive wheels Prime": "303011",
    "Drive wheels PUR": "303012",
    "Drive wheels friction": "303013",
    "Drive wheels ESD": "303014",
    "Rollers Prime": "303021",
    "Rollers PUR": "303022",
    "Rollers friction": "303023",
    "Support arm wheels Prime": "303041",
    "Support arm wheels ESD": "303042",
    "Support arm wheels PUR": "303043",
    "Wheels": "210000",
    "Drive wheels": "210100",
    "Rollers": "210200",
    "Support arm wheels": "210400",
    "Miscellaneous": "303019",
    "Seats": "601020",
    "Finished products": "220000",
    "Seat": "220300",
    "Sensors": "103004",
    "Electronics": "110000",
    "Electronic components": "110300",
    "Maintenance and operating of sites": "09",
    "Sites maintenance and operating": "09-01",
    "Maintenance of buildings": "09-02",
    "Surveillance, safety and security": "09-03",
    "Safety": "09-04",
    "Security": "09-05",
    "Cleaning and desinfecting": "09-06",
    "Facility management": "09-07"
}



# """{
#     "certification_authority": ""
#     "certificate_type": ""
#     "certification_date_valid_from": ""
#     "certification_date_valid_to": ""
#     "company_name": ""
#     "company_address": ""
#     "expiration_date": ""
# }"""

logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)

def extract_certificate_type(llm_certificate_type_extraction):
    for certificate_type_key, certificate_type_value in CERTIFICATE_TYPES.items():
        logger.info("certificate_type_key: " + str(certificate_type_key))
        if certificate_type_key in llm_certificate_type_extraction:
            logger.info("certificate_type_value: " + str(certificate_type_value))
            return certificate_type_value
    return llm_certificate_type_extraction



def set_standard_certificate_type(extracted_document_data_complete):
    logger.info("set_standard_certificate_type extracted_document_data_complete: " + str(extracted_document_data_complete))
    if not extracted_document_data_complete:
        return {}

    if (extracted_document_data_complete.get("extracted_document_data_complete", None)
        and extracted_document_data_complete.get("extracted_document_data_complete", None).get("certificate_type", None)):
        certificate_type = extracted_document_data_complete["extracted_document_data_complete"]["certificate_type"]
        extracted_document_data_complete["extracted_document_data_complete"]["certificate_type"] = extract_certificate_type(certificate_type)
        logger.info("set_standard_certificate_type done: " + str(extracted_document_data_complete))
    return extracted_document_data_complete



def add_extracted_structured_data(extracted_document_data_complete,
                                  extracted_structured_data: BaseModel):
    if not extracted_structured_data:
        return {}

    if not extracted_document_data_complete:
        extracted_document_data_complete = dict()

    if (not extracted_document_data_complete.get("certification_authority", None)
            and extracted_structured_data.certification_authority):
        extracted_document_data_complete["certification_authority"] = extracted_structured_data.certification_authority

    if (not extracted_document_data_complete.get("certificate_type", None)
            and extracted_structured_data.certificate_type):
        extracted_document_data_complete["certificate_type"] = extracted_structured_data.certificate_type

    if (not extracted_document_data_complete.get("certification_date_valid_from", None)
            and extracted_structured_data.certification_date_valid_from):
        extracted_document_data_complete[
            "certification_date_valid_from"] = extracted_structured_data.certification_date_valid_from

    if (not extracted_document_data_complete.get("certification_date_valid_to", None)
            and extracted_structured_data.certification_date_valid_to):
        extracted_document_data_complete[
            "certification_date_valid_to"] = extracted_structured_data.certification_date_valid_to

    if (not extracted_document_data_complete.get("company_name", None)
            and extracted_structured_data.company_name):
        extracted_document_data_complete["company_name"] = extracted_structured_data.company_name

    if (not extracted_document_data_complete.get("company_address", None)
            and extracted_structured_data.company_address):
        extracted_document_data_complete["company_address"] = extracted_structured_data.company_address

    if (not extracted_document_data_complete.get("expiration_date", None)
            and extracted_structured_data.expiration_date):
        extracted_document_data_complete["expiration_date"] = extracted_structured_data.expiration_date

    if (not extracted_document_data_complete.get("material_group", None)
            and extracted_structured_data.material_group):
        extracted_document_data_complete["material_group"] = extracted_structured_data.material_group

    if (not extracted_document_data_complete.get("all_important_fields", None)
            and extracted_structured_data.all_important_fields):
        extracted_document_data_complete["all_important_fields"] = extracted_structured_data.all_important_fields

    return extracted_document_data_complete


def add_polygon_for_data(extracted_document_data_complete, word_polygon):
    print("add_polygon_for_data extracted_document_data_complete " + str(extracted_document_data_complete))
    print("extracted_document_data_complete word_polygon " + str(word_polygon))

    if not extracted_document_data_complete:
        return {}

    certification_authority = extracted_document_data_complete.get("certification_authority", None)
    if certification_authority:
        extracted_document_data_complete["certification_authority_polygon"] = get_polygon_of_text_sequence(certification_authority, word_polygon)

    certificate_type = extracted_document_data_complete.get("certificate_type", None)
    if certificate_type:
        extracted_document_data_complete["certificate_type_polygon"] = get_polygon_of_text_sequence(certificate_type, word_polygon)

    certification_date_valid_from = extracted_document_data_complete.get("certification_date_valid_from", None)
    if certification_date_valid_from:
        extracted_document_data_complete["certification_date_valid_from_polygon"] = get_polygon_of_text_sequence(certification_date_valid_from, word_polygon)

    certification_date_valid_to = extracted_document_data_complete.get("certification_date_valid_to", None)
    if certification_date_valid_to:
        extracted_document_data_complete["certification_date_valid_to_polygon"] = get_polygon_of_text_sequence(certification_date_valid_to, word_polygon)

    company_name = extracted_document_data_complete.get("company_name", None)
    if company_name:
        extracted_document_data_complete["company_name_polygon"] = get_polygon_of_text_sequence(company_name, word_polygon)

    company_address = extracted_document_data_complete.get("company_address", None)
    if company_address:
        extracted_document_data_complete["company_address_polygon"] = get_polygon_of_text_sequence(company_address, word_polygon)

    expiration_date = extracted_document_data_complete.get("expiration_date", None)
    if expiration_date:
        extracted_document_data_complete["expiration_date_polygon"] = get_polygon_of_text_sequence(expiration_date, word_polygon)

    return extracted_document_data_complete

def get_polygon_of_text_sequence(text_sequence, word_polygon_dict):
    polygons_list = list()
    words = text_sequence.split(' ')
    print("get_polygon_of_text_sequence polygons_list " + str(polygons_list))
    for word in words:
        print("get_polygon_of_text_sequence word "+word)
        if word_polygon_dict.get(word, None):
            polygons_list.append(word_polygon_dict[word])
    return polygons_list



def add_extracted_data1(extracted_document_data_complete, extracted_document_data):
    if not extracted_document_data:
        return {}
    try:
        extracted_document_data = json.loads(extracted_document_data)
    except Exception as e:
        self.logger.error("add_extracted_data "+str(e))
        extracted_document_data = None

    if not extracted_document_data:
        return {}

    if not extracted_document_data_complete:
        extracted_document_data_complete = dict()

    if (not extracted_document_data_complete.get("certification_authority", None)
            and extracted_document_data.get("certification_authority", None)):
        extracted_document_data_complete["certification_authority"] = extracted_document_data.get("certification_authority", None)

    if (not extracted_document_data_complete.get("certificate_type", None)
            and extracted_document_data.get("certificate_type", None)):
        extracted_document_data_complete["certificate_type"] = extracted_document_data.get("certificate_type", None)

    if (not extracted_document_data_complete.get("certification_date_valid_from", None)
            and extracted_document_data.get("certification_date_valid_from", None)):
        extracted_document_data_complete["certification_date_valid_from"] = extracted_document_data.get("certification_date_valid_from", None)

    if (not extracted_document_data_complete.get("certification_date_valid_to", None)
            and extracted_document_data.get("certification_date_valid_to", None)):
        extracted_document_data_complete["certification_date_valid_to"] = extracted_document_data.get("certification_date_valid_to", None)

    if (not extracted_document_data_complete.get("company_name", None)
            and extracted_document_data.get("company_name", None)):
        extracted_document_data_complete["company_name"] = extracted_document_data.get("company_name", None)

    if (not extracted_document_data_complete.get("company_address", None)
            and extracted_document_data.get("company_address", None)):
        extracted_document_data_complete["company_address"] = extracted_document_data.get("company_address", None)

    if (not extracted_document_data_complete.get("expiration_date", None)
            and extracted_document_data.get("expiration_date", None)):
        extracted_document_data_complete["expiration_date"] = extracted_document_data.get(
            "expiration_date", None)
    return extracted_document_data_complete


def find_closest_match_in_text(text, choices):
    matches_list = list()
    sequences_list = generate_list_of_sequences(text, choices)
    for choice in choices:
        result = process.extractOne(choice, sequences_list)
        closest_match, score, index = result[0], result[1], result[2]
        print("find_closest_match_in_text "+str(choice)+" closest match: "+str(closest_match)+" score: "+str(score))
        matches_list.append(str(result))
    return matches_list



def generate_list_of_sequences(text, choices):

    max_choice_length = max(len(list(choice.split())) for choice in choices)

    text_words_list = list(text.split())

    sequences_list = list()
    for current_word_index, current_word in enumerate(text_words_list):
        current_sequence = ""
        for i in range(max_choice_length):
            if current_word_index+i < len(text_words_list):
                current_sequence = current_sequence +" "+ text_words_list[current_word_index+i]
        sequences_list.append(current_sequence)
    return sequences_list


# Function to find closest match
def find_closest_match_1(query, choices):
    result = rapidfuzzProcess.extractOne(query, choices)
    closest_match, score = result[0], result[1]
    return closest_match

def find_closest_match(query, choices):
    # Get a list of matches ordered by score, default limit to 5

    # Str1 = "My name is Ali"
    # Str2 = "Ali is my name name"
    # print(fuzz.token_sort_ratio(Str1, Str2))
    # print(fuzz.token_set_ratio(Str1, Str2))
    #
    # Str1 = "My name is Ali"
    # Str2 = "Ali is my name"
    # print(fuzz.token_sort_ratio(Str1, Str2))
    #
    # Str1 = "My name is Ali"
    # Str2 = "My name is Ali Abdaal"
    # print(fuzz.partial_ratio(Str1.lower(), Str2.lower()))
    #
    # result = process.extract(query, choices)

    result = fuzzywuzzyProcess.extractOne(query, choices)
    closest_match, score = result[0], result[1]
    return closest_match