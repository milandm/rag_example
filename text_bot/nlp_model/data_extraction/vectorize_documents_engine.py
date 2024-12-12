import sys

sys.path.append("..")

from text_bot.nlp_model.nlp_model import NlpModel
from text_bot.utils import load_documents, save_json_to_file, load_json_file

# SENTENCE_MIN_LENGTH = 15
SENTENCE_MIN_LENGTH = 2

from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from text_bot.views.models import CTDocument, \
    CTDocumentSplit, \
    CTDocumentPage, \
    QuotesDocuments


from text_bot.nlp_model.data_extraction.prompt_creator import PromptCreator
from text_bot.utils import (load_and_ocr_documents_with_filename,
                            load_document_paths,
                            load_pdf_pages_to_files)
from text_bot.nlp_model.ngrams_utils import map_di_words_to_fields
from custom_logger.universal_logger import UniversalLogger
import json
from text_bot.nlp_model.llm_structured_output_models.certificate_extraction_model import CertificateExtractionModel
from text_bot.nlp_model.llm_structured_output_models.certificate_extraction_with_material_model import CertificateExtractionWithMaterialModel
from text_bot.nlp_model.llm_structured_output_models.evaluation_extraction_model import EvaluationExtractionModel
from text_bot.nlp_model.data_extraction.data_mapping import (add_extracted_structured_data,
                                                             set_standard_certificate_type,
                                                             MATERIAL_GROUPS,
                                                             find_closest_match,
                                                             OFFICIAL_COMPANY_NAMES)
from text_bot.nlp_model.spacy_model import extract_information, get_langugage
from text_bot.nlp_model.document_inteligence import DocumentIntelligence
from text_bot.nlp_model.spacy_anonymizer import SpacyAnonymizer
from text_bot.nlp_model.table_extractor import TableExtractor
from text_bot.nlp_model.pdf_table_extractor import PDFTableExtractor


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


    def load_documents(self):
        self.logger.info("load_documents")
        self.extract_data_using_ocr()


    def load_all_tabular_data_from_pdf(self):

        document_files = load_document_paths("documents_to_vectorize/")

        # image_pages_list = list()
        # for document_file in document_files:
        #     document_image_pages_list = load_pdf_pages_to_files(document_file)
        #     image_pages_list.extend(document_image_pages_list)

        for document_file_path in document_files:
            extractor = PDFTableExtractor(document_file_path)
            json_data = extractor.run()
            self.logger.info("extracted_table_data: "+str(json_data))


    def load_tabular_data_from_pdf(self):

        document_files  = load_document_paths()


        image_pages_list = list()
        for document_file in document_files:
            document_image_pages_list = load_pdf_pages_to_files(document_file)
            image_pages_list.extend(document_image_pages_list)

        for document_image in image_pages_list:
            # Initialize with your image path
            extractor = TableExtractor(document_image)

            # Extract table data
            data = extractor.extract_table()
            print(str(data))

            # Convert to DataFrame
            df = extractor.to_dataframe()

            # Display the DataFrame
            print(df)


    def count_not_extracted_fields(self):
        documents_extraction_evaluation_list = list()

        ocr_extractions_none_count = dict()
        di_extractions_none_count = dict()

        ocr_document_extractions_list = load_json_file("json_export_evaluation/ocr_export/json_merged_20240913_102112.json")
        di_document_extractions_list = load_json_file("json_export_evaluation/di_export/json_document_intelligence_di_20240913_112408.json")

        for ocr_extraction in ocr_document_extractions_list:
            ocr_extracted_data = ocr_extraction["extracted_document_data_complete"]

            self.increment_field_count("certificate_type", ocr_extracted_data, ocr_extractions_none_count)
            self.increment_field_count("certification_date_valid_from", ocr_extracted_data, ocr_extractions_none_count)
            self.increment_field_count("certification_date_valid_to", ocr_extracted_data, ocr_extractions_none_count)
            self.increment_field_count("company_name", ocr_extracted_data, ocr_extractions_none_count)
            self.increment_field_count("company_address", ocr_extracted_data, ocr_extractions_none_count)
            self.increment_field_count("material_group", ocr_extracted_data, ocr_extractions_none_count)
            self.increment_field_count("official_company_name", ocr_extracted_data, ocr_extractions_none_count)



        for di_extraction in di_document_extractions_list:
            di_extracted_data = di_extraction["extracted_document_data_complete"]

            self.increment_field_count("certificate_type", di_extracted_data, di_extractions_none_count)
            self.increment_field_count("certification_date_valid_from", di_extracted_data, di_extractions_none_count)
            self.increment_field_count("certification_date_valid_to", di_extracted_data, di_extractions_none_count)
            self.increment_field_count("company_name", di_extracted_data, di_extractions_none_count)
            self.increment_field_count("company_address", di_extracted_data, di_extractions_none_count)
            self.increment_field_count("material_group", di_extracted_data, di_extractions_none_count)
            self.increment_field_count("official_company_name", di_extracted_data, di_extractions_none_count)


        self.logger.info("ocr_extractions_none_count: "+str(ocr_extractions_none_count))
        self.logger.info("di_extractions_none_count: " + str(di_extractions_none_count))



    def increment_field_count(self, field_name, extracted_data, count_dict):
        field_value = extracted_data.get(field_name, None)

        not_recognized_list=[
        "N/A"
        "Not provided",
        "Not specified",
        "Not explicitly provided",
        "Unknown"]

        if field_name == "material_group":
            if field_value and not field_value in not_recognized_list:
                field_value_list = field_value.split(",")
                field_value = field_value_list[0].trim
                if not field_value in MATERIAL_GROUPS:
                    field_value = None

        if not field_value or field_value in not_recognized_list:
            count = count_dict.get(field_name, 0)
            count_dict[field_name] = count + 1




    def count_fields_marked_as_failed_by_llm(self):
        formatted_json_data = load_json_file("json_export/formatted_data.json")

        ocr_failed_fields = dict()
        di_failed_fields = dict()

        for entry in formatted_json_data:
            for ocr_failed_field in entry["ocr_failed_fields"].split(","):
                self.logger.info("ocr_failed_field: " + str(ocr_failed_field))
                ocr_failed_fields_count = ocr_failed_fields.get(ocr_failed_field,0)
                ocr_failed_fields[ocr_failed_field] = ocr_failed_fields_count+1

            for di_failed_field in entry["di_failed_fields"].split(","):
                self.logger.info("di_failed_field: " + str(di_failed_field))
                di_failed_fields_count = di_failed_fields.get(di_failed_field,0)
                di_failed_fields[di_failed_field] = di_failed_fields_count+1

        self.logger.info("ocr_failed_fields: " + str(ocr_failed_fields))
        self.logger.info("di_failed_fields: " + str(di_failed_fields))



    def fix_evaluation_json_export(self):
        raw_json_data = load_json_file("json_export/json_evaluation_extraction_20240915_191031.json")

        # Convert the list of JSON strings to a list of dictionaries
        formatted_json_data = [json.loads(entry) for entry in raw_json_data]

        # Output the formatted JSON
        formatted_json = json.dumps(formatted_json_data, indent=4)

        # Print the formatted JSON
        print(formatted_json)

        # Optionally, write to a file
        with open("formatted_data.json", "w") as json_file:
            json_file.write(formatted_json)


    def evaluate_di_and_ocr_exports(self):
        documents_extraction_evaluation_list = list()

        ocr_document_extractions_list = load_json_file("json_export_evaluation/ocr_export/json_merged_20240913_102112.json")
        di_document_extractions_list = load_json_file("json_export_evaluation/di_export/json_document_intelligence_di_20240913_112408.json")

        paired_list = list(zip(ocr_document_extractions_list, di_document_extractions_list))

        for extraction_pair in paired_list:

            ocr_document_extractions = extraction_pair[0]

            di_document_extractions = extraction_pair[1]
            extracted_document_data_complete = di_document_extractions.get("extracted_document_data_complete", None)
            if extracted_document_data_complete:
                extracted_document_data_complete.pop('certification_authority_polygon', None)
                extracted_document_data_complete.pop('certificate_type_polygon', None)
                extracted_document_data_complete.pop('certification_date_valid_from_polygon', None)
                extracted_document_data_complete.pop('certification_date_valid_to_polygon', None)
                extracted_document_data_complete.pop('company_name_polygon', None)
                extracted_document_data_complete.pop('company_address_polygon', None)
                extracted_document_data_complete.pop('expiration_date_polygon', None)

            self.logger.info("ocr_document_extractions: " + str(ocr_document_extractions))
            self.logger.info("di_document_extractions: " + str(di_document_extractions))

            document_extraction_evaluation = (
                self.prompt_creator.evaluate_document_extraction(ocr_document_extractions,
                                                                 di_document_extractions,
                                                                 EvaluationExtractionModel))

            self.logger.info("document_extraction_evaluation: " + str(document_extraction_evaluation))
            documents_extraction_evaluation_list.append(document_extraction_evaluation)

        self.logger.info("documents_extraction_evaluation_list: "+str(documents_extraction_evaluation_list))
        save_json_to_file(documents_extraction_evaluation_list, "json_export/json_evaluation_extraction")





    def fuzzy_match_exported_companies_names(self):
        documents_extraction_list = list()
        companies_list = list()
        document_extractions = load_json_file("json_export/json_document_intelligence_20240912_150934.json")
        for document_extraction in document_extractions:
            document_content = document_extraction.get("documents_content", None)
            extracted_document_data_complete = document_extraction.get("extracted_document_data_complete", None)
            if extracted_document_data_complete:
                company_name = extracted_document_data_complete.get("company_name", None)
                material_group = extracted_document_data_complete.get("material_group", None)
                official_company_name = find_closest_match(company_name, list(OFFICIAL_COMPANY_NAMES))
                document_extraction = {"company_name": company_name,
                                       "material_group":material_group,
                                       "official_company_name": official_company_name,
                                       "document_content":document_content}
                documents_extraction_list.append(document_extraction)
                companies_list.append(company_name)
        self.logger.info("companies_list: "+str(companies_list))
        save_json_to_file(documents_extraction_list, "json_export/json_document_intelligence_diff")



    def export_material_group(self):
        documents_extraction_list = list()
        document_extractions = load_json_file("json_export/json_document_intelligence_20240912_075444.json")
        for document_extraction in document_extractions:
            document_content = document_extraction.get("documents_content", None)
            extracted_document_data_complete = document_extraction.get("extracted_document_data_complete", None)
            if extracted_document_data_complete:
                material_group = extracted_document_data_complete.get("material_group", None)
                document_extraction = {"material_group": material_group,"document_content": document_content}
                documents_extraction_list.append(document_extraction)
        save_json_to_file(documents_extraction_list, "json_export/json_document_intelligence_diff_material")



    def extract_data_using_di(self):

        document_intelligence = DocumentIntelligence()

        document_paths = load_document_paths("documents_to_vectorize/")
        documents_extraction_list = list()
        for document_path_and_filename in document_paths:
            documents_extraction = document_intelligence.extract_key_value_pairs(document_path_and_filename)

            document_data_complete = dict()
            document_data_complete["documents_content"] = documents_extraction["words_concatenation"]
            document_data_complete["file_name"] = documents_extraction["path_to_sample_documents"]
            document_data_complete["word_polygon"] = documents_extraction["word_polygon"]
            extracted_document_data, confidence_levels = self.prompt_creator.extract_document_data_structured_output(document_data_complete["documents_content"],
                                                                                                  CertificateExtractionModel)

            extracted_document_data_complete = add_extracted_structured_data(extracted_document_data_complete, extracted_document_data)
            document_data_complete["extracted_document_data_complete"] = extracted_document_data_complete
            document_data_complete = set_standard_certificate_type(document_data_complete)
            document_data_complete["nlp_confidence_levels"] = confidence_levels

            documents_extraction_list.append(document_data_complete)

        save_json_to_file(documents_extraction_list, "json_export/json_document_intelligence")


    def anonymize_data(self):

        document_intelligence = DocumentIntelligence()
        spacy_anonymizer = SpacyAnonymizer()


        document_paths = load_document_paths("documents_to_vectorize/")
        documents_extraction_list = list()
        for document_path_and_filename in document_paths:
            documents_extraction, words_confidence = document_intelligence.analyze_read(document_path_and_filename)

            documents_extraction_anonymize = spacy_anonymizer.anonymize(documents_extraction["words_concatenation"])

            documents_extraction_list.append(documents_extraction_anonymize)

        save_json_to_file(documents_extraction_list, "json_export/json_document_intelligence")



    def extract_data_using_di_recognize_materials(self):

        document_intelligence = DocumentIntelligence()

        document_paths = load_document_paths("documents_to_vectorize/")
        documents_extraction_list = list()

        # companies_names_list = list()

        for document_path_and_filename in document_paths:
            documents_extraction, words_confidence = document_intelligence.analyze_read(document_path_and_filename)

            if documents_extraction.get('word_polygon', None):
                documents_extraction.pop('word_polygon', None)

            self.logger.info("documents_extraction " + str(documents_extraction))

            document_data_complete = dict()
            document_data_complete["documents_content"] = documents_extraction["words_concatenation"]
            document_data_complete["file_name"] = documents_extraction["path_to_sample_documents"]
            # document_data_complete["word_polygon"] = documents_extraction["word_polygon"]
            extracted_document_data, confidence_levels = (
                self.prompt_creator.extract_document_data_structured_output_material_groups_list(document_data_complete["documents_content"],
                                                                                                  CertificateExtractionWithMaterialModel,
                                                                                                 MATERIAL_GROUPS))

            di_export_confidence = map_di_words_to_fields(words_confidence, extracted_document_data)

            # extracted_document_data = (
            #     self.prompt_creator.extract_document_data_structured_output(document_data_complete["documents_content"],
            #                                                                                       CertificateExtractionModel))

            self.logger.info("extracted confidence_levels: "+ str(confidence_levels))

            extracted_document_data_complete = dict()
            extracted_document_data_complete = add_extracted_structured_data(extracted_document_data_complete, extracted_document_data)
            # extracted_document_data_complete = add_polygon_for_data(extracted_document_data_complete, documents_extraction["word_polygon"])
            document_data_complete["extracted_document_data_complete"] = extracted_document_data_complete
            document_data_complete["nlp_confidence_levels"] = confidence_levels
            document_data_complete["di_confidence_levels"] = di_export_confidence
            document_data_complete = set_standard_certificate_type(document_data_complete)

            # document_data_complete["find_closest_match_in_text"] = find_closest_match_in_text(document_data_complete["documents_content"], MATERIAL_GROUPS)


            # pronaci sve entitete koji mogu da budu trazeni entiteti, pronaci sve entitete koji mogu biti labele,
            # to sve dodati u prompt i onda na kraju uporediti da li su izvucene vrednosti dobre

            company_name = extracted_document_data_complete.get("company_name", None)
            if company_name:
                document_data_complete["extracted_document_data_complete"]["official_company_name"] = find_closest_match(company_name, list(OFFICIAL_COMPANY_NAMES))

            # if (document_data_complete.get("extracted_document_data_complete", None)
            #         and document_data_complete["extracted_document_data_complete"].get("company_name", None)):
            #     companies_names_list.append(document_data_complete["extracted_document_data_complete"]["company_name"])

            documents_extraction_list.append(document_data_complete)

        # self.logger.info("companies_names_list " + str(companies_names_list))

        save_json_to_file(documents_extraction_list, "json_export/json_document_intelligence_di")



    def extract_data_ner(self):
        extracted_documents_data_list = list()
        document_pages_content = load_and_ocr_documents_with_filename("documents_to_vectorize/")

        for document_page_content in document_pages_content:

            filename = document_page_content["filename"]
            plain_text_content_pages = document_page_content["plain_text_content_pages"]
            ocr_text_content_pages = document_page_content["ocr_text_content_pages"]
            words_confidence_levels = document_page_content["words_confidence_levels"]

            document_data_complete = dict()
            extracted_document_data_complete = dict()

            for plain_text_page_content in plain_text_content_pages:
                if plain_text_page_content:
                    language = get_langugage(plain_text_page_content)
                    self.logger.info("pdf_loaded language " + str(language))
                    extracted_document_data = extract_information(language, plain_text_page_content)
                    self.logger.info("pdf_loaded extracted_document_data " + str(extracted_document_data))

            for ocr_text_page_content in ocr_text_content_pages:
                if ocr_text_page_content:
                    language = get_langugage(ocr_text_page_content)
                    self.logger.info("ocr_loaded language " + str(language))
                    extracted_document_data = extract_information(language, ocr_text_page_content)
                    self.logger.info("ocr_loaded extracted_document_data " + str(extracted_document_data))



    def extract_data_using_ocr(self):
        extracted_documents_data_list = list()
        document_pages_content = load_and_ocr_documents_with_filename("documents_to_vectorize/")

        for document_page_content in document_pages_content:

            filename = document_page_content["filename"]
            plain_text_content_pages = document_page_content["plain_text_content_pages"]
            ocr_text_content_pages = document_page_content["ocr_text_content_pages"]
            # words_confidence_levels = document_page_content["words_confidence_levels"]

            # self.logger.info("words_confidence_levels: " + str(words_confidence_levels))
            # self.logger.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!words_confidence_levels!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # self.logger.info("words_confidence_levels: " + str(words_confidence_levels))

            document_data_complete = dict()
            extracted_document_data_complete = dict()
            for plain_text_page_content in plain_text_content_pages:
                if plain_text_page_content:
                    document_data_complete["pdf_loaded"] = plain_text_page_content
                    # extracted_document_data = self.prompt_creator.extract_document_data_structured_output(pdf_loaded, CertificateExtractionModel)

                    extracted_document_data, confidence_levels = (
                        self.prompt_creator.extract_document_data_structured_output_material_groups_list(
                            plain_text_page_content,
                            CertificateExtractionWithMaterialModel,
                            MATERIAL_GROUPS))
                    self.logger.info("extracted_document_data " + str(extracted_document_data))
                    extracted_document_data_complete = add_extracted_structured_data(extracted_document_data_complete, extracted_document_data)
                    document_data_complete["pdf_nlp_confidence_levels"] = confidence_levels

            for ocr_text_page_content in ocr_text_content_pages:
                if ocr_text_page_content:
                    document_data_complete["ocr_text_page_content"] = ocr_text_page_content
                    # extracted_document_data = self.prompt_creator.extract_document_data_structured_output(ocr_loaded, CertificateExtractionModel)
                    extracted_document_data, confidence_levels = (
                        self.prompt_creator.extract_document_data_structured_output_material_groups_list(
                            ocr_text_page_content,
                            CertificateExtractionWithMaterialModel,
                            MATERIAL_GROUPS))
                    self.logger.info("extracted_document_data " + str(extracted_document_data))
                    extracted_document_data_complete = add_extracted_structured_data(extracted_document_data_complete, extracted_document_data)
                    document_data_complete["ocr_nlp_confidence_levels"] = confidence_levels

                    # ocr_export_confidence ocr confidence levels calculated per output
                    # ocr_export_confidence = map_di_words_to_fields(words_confidence_levels, extracted_document_data)
                    # self.logger.info("ocr_export_confidence: " + str(ocr_export_confidence))
                    # document_data_complete["ocr_export_confidence"] = ocr_export_confidence

            # document_data_complete["ocr_export_confidence"] = words_confidence_levels
            document_data_complete["file_name"] = filename
            document_data_complete["extracted_document_data_complete"] = extracted_document_data_complete
            document_data_complete = set_standard_certificate_type(document_data_complete)

            company_name = extracted_document_data_complete.get("company_name", None)
            if company_name:
                document_data_complete["extracted_document_data_complete"]["official_company_name"] = find_closest_match(company_name, list(OFFICIAL_COMPANY_NAMES))

            extracted_documents_data_list.append(document_data_complete)
        save_json_to_file(extracted_documents_data_list, "json_export/json_merged")



    def load_documents_to_db(self):
        documents = load_documents("documents/")
        for document_pages in documents:

            document_pages_formatted = self.get_document_split_pages(document_pages)

            md_header_splits = self.markdown_splitter.split_text(document_pages_formatted)
            documents_splits = self.text_splitter.split_documents(md_header_splits)

            self.add_document_page(document_pages_formatted)
            self.add_document_splits(documents_splits)



    def load_semantic_document_chunks_to_db(self):
        documents = load_documents("documents_to_vectorize/")
        for document_pages in documents:

            document_page_formatted_list = self.get_document_split_pages(document_pages)

            for document_page_idx, document_page_formatted in enumerate(document_page_formatted_list):
                previous_last_semantic_chunk = ""
                if not self.page_already_added_to_db(document_page_formatted, document_page_idx):
                    documents_splits = self.recursive_text_splitter.split_documents([document_page_formatted])
                    previous_last_semantic_chunk = self.add_semantic_document_splits(documents_splits, previous_last_semantic_chunk, document_page_idx)
                    self.add_document_page(document_page_formatted, document_page_idx)


    def splits_already_added_to_db(self, ct_document, documents_splits):
        old_document_splits_count = ct_document.document_splits.all().count()
        return old_document_splits_count >= len(documents_splits)


    def page_index_already_added_to_db(self, ct_document, documents_page_index):
        old_document_pages_count = ct_document.document_pages.all().count()
        return old_document_pages_count > documents_page_index


    def get_document_split_pages(self, document_pages):
        for document_page in document_pages:
            if len(document_page.page_content) > MAX_PAGE_SIZE:
                return self.pages_splitter.split_documents(document_pages)
        return document_pages


    def get_document(self, documents_split):
        document_filename = documents_split.metadata.get("source", "")

        ct_document = None
        try:
            ct_document = CTDocument.objects.get(document_filename=document_filename)
        except CTDocument.DoesNotExist as e:
            print(e)

        if not ct_document:
            ct_document = self.create_new_document(documents_split)
        return ct_document


    def create_new_document(self, documents_split):
        document_title = self.prompt_creator.get_document_title(documents_split.page_content)
        document_filename = documents_split.metadata.get("source", "")

        print("Document title: ", document_title)
        print("Document filename: ", document_filename)

        ct_document = CTDocument.objects.create(
            document_version="1",
            document_title=document_title,
            document_filename=document_filename)

        return ct_document

    def add_document_page(self, document_page, pages_index):
        ct_document = self.get_document(document_page)
        if not self.page_already_added_to_document(ct_document, pages_index):
            print("Document page content: ", document_page.page_content)
            CTDocumentPage.objects.create(
                ct_document=ct_document,
                document_page_text=document_page.page_content,
                document_page_number=pages_index)

    def page_already_added_to_document(self, ct_document, pages_index):
        old_document_pages_count = ct_document.document_pages.all().count()
        return old_document_pages_count > pages_index

    def page_already_added_to_db(self, document_page, pages_index):
        ct_document = self.get_document(document_page)
        old_document_pages_count = ct_document.document_pages.all().count()
        return old_document_pages_count > pages_index

    def add_document_splits(self, documents_splits):
        ct_document = self.get_document(documents_splits[0])
        if not self.splits_already_added_to_db(ct_document, documents_splits):
            ct_document.document_splits.all().delete()
            for i, documents_split in enumerate(documents_splits):
                document_page = documents_split.metadata.get("page", 0)
                split_text = documents_split.page_content

                embedding = self.model.get_embedding(split_text)

                CTDocumentSplit.objects.create(
                    ct_document=ct_document,
                    document_title=ct_document.document_title,
                    document_filename=ct_document.document_filename,
                    document_page=document_page,
                    split_text=split_text,
                    split_text_compression="",
                    split_number=i,
                    embedding=embedding)

    def add_semantic_document_splits(self, documents_splits, previous_last_semantic_chunk = "", document_page_idx = 0):
        ct_document = self.get_document(documents_splits[0])

        ct_document.document_sections.filter(document_page=document_page_idx).all().delete()

        section_index = 0

        if previous_last_semantic_chunk:
            previous_last_semantic_chunk.page_content = previous_last_semantic_chunk.page_content +" "+documents_splits[0].page_content
            previous_last_semantic_chunk_splits = self.recursive_text_splitter.split_documents([previous_last_semantic_chunk])
            documents_splits = previous_last_semantic_chunk_splits + documents_splits[1:]


        for i, documents_split in enumerate(documents_splits):
            # document_page = documents_split.metadata.get("page", 0)
            split_text = documents_split.page_content
            embedding = self.model.get_embedding(split_text)
            ct_document_section = QuotesDocuments.objects.create(section_text_value = split_text,
                                               text_embedding = embedding)

        return documents_splits[-1]

