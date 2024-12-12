
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult
from pyspark.sql.functions import col, flatten, regexp_replace, explode, create_map, lit

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

from custom_logger.universal_logger import UniversalLogger

import synapse.ml
from synapse.ml.cognitive import *

# endpoint = "https://<my-custom-subdomain>.cognitiveservices.azure.com/"
from text_bot.nlp_model.config import (
    DOCUMENTINTELLIGENCE_ENDPOINT,
    DOCUMENTINTELLIGENCE_API_KEY
)

# DOCUMENTINTELLIGENCE_ENDPOINT = 'https://synechronsynertradepoc.cognitiveservices.azure.com/'
# DOCUMENTINTELLIGENCE_API_KEY = 'ade4cf88fb264aa7bbdab9f032e345ab'

DOCUMENTINTELLIGENCE_ENDPOINT = 'https://synertradesynechronpoc.cognitiveservices.azure.com/'
DOCUMENTINTELLIGENCE_API_KEY = '163081d2a68843f881a2a95e739bd2dd'


class DocumentIntelligence:

    def __init__(self):
        credential = AzureKeyCredential(DOCUMENTINTELLIGENCE_API_KEY)
        self.document_intelligence_client = DocumentIntelligenceClient(endpoint=DOCUMENTINTELLIGENCE_ENDPOINT, credential=credential)
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)


    # helper functions
    def get_words(self, page, line):
        result = []
        for word in page.words:
            if self._in_span(word, line.spans):
                result.append(word)
        return result


    def _in_span(self, word, spans):
        for span in spans:
            if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
                return True
        return False

    def extract_key_value_pairs(self, path_to_sample_documents):
        # # Load the file
        # with open(file_path, "rb") as document:
        #     poller = self.document_intelligence_client.begin_analyze_document("prebuilt-layout", document)
        #     result = poller.result()

        with open(path_to_sample_documents, "rb") as f:
            poller = self.document_intelligence_client.begin_analyze_document(
                "prebuilt-layout", analyze_request=f, content_type="application/octet-stream"
            )

        result: AnalyzeResult = poller.result()

        # Extracting key-value pairs from the document
        for document in result.documents:
            print("Document:")
            for name, field in document.fields.items():
                self.logger.info(f"extract_key_value_pairs {name}: {field.value}")
                # if field.value_type == "string":
                #     print(f"{name}: {field.value}")
                # elif field.value_type == "address":
                #     print(f"{name} Address: {field.value}")

        # Extracting key-value pairs from tables if available
        for table in result.tables:
            print("Table:")
            for cell in table.cells:
                print(f"Cell ({cell.row_index}, {cell.column_index}): {cell.content}")

        # Extract other key-value pairs from different elements
        for kv_pair in result.key_value_pairs:
            print(f"Key: {kv_pair.key}, Value: {kv_pair.value}")





    def analyze_read(self, path_to_sample_documents) -> dict:

        words_confidence = list()

        documents_extraction = dict()
        # poller = self.document_intelligence_client.begin_analyze_document("prebuilt-read", AnalyzeDocumentRequest(url_source=formUrl))

        documents_extraction["path_to_sample_documents"] = path_to_sample_documents
        documents_extraction["word_polygon"] = dict()

        with open(path_to_sample_documents, "rb") as f:
            poller = self.document_intelligence_client.begin_analyze_document(
                "prebuilt-layout", analyze_request=f, content_type="application/octet-stream"
            )

        result: AnalyzeResult = poller.result()

        print("----Languages detected in the document----")
        if result.languages is not None:
            for language in result.languages:
                print(f"Language code: '{language.locale}' with confidence {language.confidence}")

        print("----Styles detected in the document----")
        if result.styles:
            for style in result.styles:
                if style.is_handwritten:
                    print("Found the following handwritten content: ")
                    print(",".join([result.content[span.offset: span.offset + span.length] for span in style.spans]))
                if style.font_style:
                    print(f"The document contains '{style.font_style}' font style, applied to the following text: ")
                    print(",".join([result.content[span.offset: span.offset + span.length] for span in style.spans]))

        for page in result.pages:
            print(f"----Analyzing document from page #{page.page_number}----")
            print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")


            if page.lines:
                for line_idx, line in enumerate(page.lines):
                    words = self.get_words(page, line)
                    print(
                        f"...Line # {line_idx} has {len(words)} words and text '{line.content}' within bounding polygon '{line.polygon}'"
                    )

                    for word in words:
                        print(f"......Word '{word.content}' has a confidence of {word.confidence}")
                        words_confidence.append(
                            {'word_content': word.content,
                             'word_confidence': word.confidence})
                        documents_extraction["word_polygon"][str(word.content)] = word.polygon

            if page.selection_marks:
                for selection_mark in page.selection_marks:
                    print(
                        f"...Selection mark is '{selection_mark.state}' within bounding polygon "
                        f"'{selection_mark.polygon}' and has a confidence of {selection_mark.confidence}"
                    )

        if result.paragraphs:
            print(f"----Detected #{len(result.paragraphs)} paragraphs in the document----")
            for paragraph in result.paragraphs:
                print(
                    f"Found paragraph with role: '{paragraph.role}' within {paragraph.bounding_regions} bounding region")
                print(f"...with content: '{paragraph.content}'")

            result.paragraphs.sort(key=lambda p: (p.spans.sort(key=lambda s: s.offset), p.spans[0].offset))
            print("-----Print sorted paragraphs-----")
            for idx, paragraph in enumerate(result.paragraphs):
                print(
                    f"...paragraph:{idx} with offset: {paragraph.spans[0].offset} and length: {paragraph.spans[0].length}"
                )

        print("----------------------------------------")

        documents_extraction["words_concatenation"] = result.content

        return documents_extraction, words_confidence



    def analyze_read_all(self, path_to_sample_documents):

        # poller = self.document_intelligence_client.begin_analyze_document("prebuilt-read", AnalyzeDocumentRequest(url_source=formUrl))

        with open(path_to_sample_documents, "rb") as f:
            poller = self.document_intelligence_client.begin_analyze_document(
                "prebuilt-layout", analyze_request=f, content_type="application/octet-stream"
            )

        result: AnalyzeResult = poller.result()

        print("----Languages detected in the document----")
        if result.languages is not None:
            for language in result.languages:
                print(f"Language code: '{language.locale}' with confidence {language.confidence}")

        print("----Styles detected in the document----")
        if result.styles:
            for style in result.styles:
                if style.is_handwritten:
                    print("Found the following handwritten content: ")
                    print(",".join([result.content[span.offset: span.offset + span.length] for span in style.spans]))
                if style.font_style:
                    print(f"The document contains '{style.font_style}' font style, applied to the following text: ")
                    print(",".join([result.content[span.offset: span.offset + span.length] for span in style.spans]))

        for page in result.pages:
            print(f"----Analyzing document from page #{page.page_number}----")
            print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

            if page.lines:
                for line_idx, line in enumerate(page.lines):
                    words = self.get_words(page, line)
                    print(
                        f"...Line # {line_idx} has {len(words)} words and text '{line.content}' within bounding polygon '{line.polygon}'"
                    )

                    for word in words:
                        print(f"......Word '{word.content}' has a confidence of {word.confidence}")

            if page.selection_marks:
                for selection_mark in page.selection_marks:
                    print(
                        f"...Selection mark is '{selection_mark.state}' within bounding polygon "
                        f"'{selection_mark.polygon}' and has a confidence of {selection_mark.confidence}"
                    )

        if result.paragraphs:
            print(f"----Detected #{len(result.paragraphs)} paragraphs in the document----")
            for paragraph in result.paragraphs:
                print(
                    f"Found paragraph with role: '{paragraph.role}' within {paragraph.bounding_regions} bounding region")
                print(f"...with content: '{paragraph.content}'")

            result.paragraphs.sort(key=lambda p: (p.spans.sort(key=lambda s: s.offset), p.spans[0].offset))
            print("-----Print sorted paragraphs-----")
            for idx, paragraph in enumerate(result.paragraphs):
                print(
                    f"...paragraph:{idx} with offset: {paragraph.spans[0].offset} and length: {paragraph.spans[0].length}"
                )

        print("----------------------------------------")




    def read_document(self, document_path):

        imageDf = spark.createDataFrame([
            (document_path,)
        ], ["source", ])

        analyzeLayout = (AnalyzeLayout()
                         .setLinkedService(ai_service_name)
                         .setImageUrlCol("source")
                         .setOutputCol("layout")
                         .setConcurrency(5))

        analyze_layout = ((((((analyzeLayout.transform(imageDf)
                          .withColumn("lines", flatten(col("layout.analyzeResult.readResults.lines"))))
                          .withColumn("readLayout", col("lines.text")))
                          .withColumn("tables", flatten(col("layout.analyzeResult.pageResults.tables"))))
                          .withColumn("cells", flatten(col("tables.cells"))))
                          .withColumn("pageLayout", col("cells.text")))
                          .select("source", "readLayout", "pageLayout"))


        self.logger.info("read_document: "+str(analyzeLayout))



    def extract_layouts(self, path_to_sample_documents):
        with open(path_to_sample_documents, "rb") as f:
            poller = self.document_intelligence_client.begin_analyze_document(
                "prebuilt-layout", analyze_request=f, content_type="application/octet-stream"
            )
        result: AnalyzeResult = poller.result()

        if result.styles and any([style.is_handwritten for style in result.styles]):
            print("Document contains handwritten content")
        else:
            print("Document does not contain handwritten content")

        for page in result.pages:
            print(f"----Analyzing layout from page #{page.page_number}----")
            print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

            if page.lines:
                for line_idx, line in enumerate(page.lines):
                    words = self.get_words(page, line)
                    print(
                        f"...Line # {line_idx} has word count {len(words)} and text '{line.content}' "
                        f"within bounding polygon '{line.polygon}'"
                    )

                    for word in words:
                        print(f"......Word '{word.content}' has a confidence of {word.confidence}")

            if page.selection_marks:
                for selection_mark in page.selection_marks:
                    print(
                        f"Selection mark is '{selection_mark.state}' within bounding polygon "
                        f"'{selection_mark.polygon}' and has a confidence of {selection_mark.confidence}"
                    )

        if result.tables:
            for table_idx, table in enumerate(result.tables):
                print(f"Table # {table_idx} has {table.row_count} rows and " f"{table.column_count} columns")
                if table.bounding_regions:
                    for region in table.bounding_regions:
                        print(f"Table # {table_idx} location on page: {region.page_number} is {region.polygon}")
                for cell in table.cells:
                    print(f"...Cell[{cell.row_index}][{cell.column_index}] has text '{cell.content}'")
                    if cell.bounding_regions:
                        for region in cell.bounding_regions:
                            print(
                                f"...content on page {region.page_number} is within bounding polygon '{region.polygon}'")

        print("----------------------------------------")




    def read_documents(self, path_to_sample_documents: str) -> dict:
        with open(path_to_sample_documents, "rb") as f:
            poller = self.document_intelligence_client.begin_analyze_document(
                "prebuilt-layout",
                analyze_request=f,
                features=[DocumentAnalysisFeature.KEY_VALUE_PAIRS],
                content_type="application/octet-stream",
            )
        result: AnalyzeResult = poller.result()

        print("----Key-value pairs found in document----")
        if result.key_value_pairs:
            for kv_pair in result.key_value_pairs:
                if kv_pair.key:
                    print(f"Key '{kv_pair.key.content}' found within " f"'{kv_pair.key.bounding_regions}' bounding regions")
                if kv_pair.value:
                    print(
                        f"Value '{kv_pair.value.content}' found within "
                        f"'{kv_pair.value.bounding_regions}' bounding regions\n"
                    )

        for page in result.pages:
            print(f"----Analyzing document from page #{page.page_number}----")
            print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

            if page.lines:
                for line_idx, line in enumerate(page.lines):
                    words = self.get_words(page.words, line)
                    print(
                        f"...Line #{line_idx} has {len(words)} words and text '{line.content}' within "
                        f"bounding polygon '{line.polygon}'"
                    )

                    for word in words:
                        print(f"......Word '{word.content}' has a confidence of {word.confidence}")






# # https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/use-sdk-rest-api?view=doc-intel-2.1.0&preserve-view=true&tabs=linux&pivots=programming-language-python
#
# # Train model without labels
# # To train a model you need an Azure Storage account.
# # Use the SAS URL to access your training files.
# trainingDataUrl = "PASTE_YOUR_SAS_URL_OF_YOUR_FORM_FOLDER_IN_BLOB_STORAGE_HERE"
#
# poller = form_training_client.begin_training(trainingDataUrl, use_training_labels=False)
# model = poller.result()
#
# print("Model ID: {}".format(model.model_id))
# print("Status: {}".format(model.status))
# print("Training started on: {}".format(model.training_started_on))
# print("Training completed on: {}".format(model.training_completed_on))
#
# print("\nRecognized fields:")
# for submodel in model.submodels:
#     print(
#         "The submodel with form type '{}' has recognized the following fields: {}".format(
#             submodel.form_type,
#             ", ".join(
#                 [
#                     field.label if field.label else name
#                     for name, field in submodel.fields.items()
#                 ]
#             ),
#         )
#     )
#
# # Training result information
# for doc in model.training_documents:
#     print("Document name: {}".format(doc.name))
#     print("Document status: {}".format(doc.status))
#     print("Document page count: {}".format(doc.page_count))
#     print("Document errors: {}".format(doc.errors))
#
#
# # Train model with labels
# # To train a model you need an Azure Storage account.
# # Use the SAS URL to access your training files.
# trainingDataUrl = "PASTE_YOUR_SAS_URL_OF_YOUR_FORM_FOLDER_IN_BLOB_STORAGE_HERE"
#
# poller = form_training_client.begin_training(trainingDataUrl, use_training_labels=True)
# model = poller.result()
# trained_model_id = model.model_id
#
# print("Model ID: {}".format(trained_model_id))
# print("Status: {}".format(model.status))
# print("Training started on: {}".format(model.training_started_on))
# print("Training completed on: {}".format(model.training_completed_on))
#
# print("\nRecognized fields:")
# for submodel in model.submodels:
#     print(
#         "The submodel with form type '{}' has recognized the following fields: {}".format(
#             submodel.form_type,
#             ", ".join(
#                 [
#                     field.label if field.label else name
#                     for name, field in submodel.fields.items()
#                 ]
#             ),
#         )
#     )
#
# # Training result information
# for doc in model.training_documents:
#     print("Document name: {}".format(doc.name))
#     print("Document status: {}".format(doc.status))
#     print("Document page count: {}".format(doc.page_count))
#     print("Document errors: {}".format(doc.errors))
#
#
#
#
# poller = form_recognizer_client.begin_recognize_custom_forms_from_url(
#     model_id=trained_model_id, form_url=formUrl)
# result = poller.result()
#
# for recognized_form in result:
#     print("Form type: {}".format(recognized_form.form_type))
#     for name, field in recognized_form.fields.items():
#         print("Field '{}' has label '{}' with value '{}' and a confidence score of {}".format(
#             name,
#             field.label_data.text if field.label_data else name,
#             field.value,
#             field.confidence
#         ))