import sys

sys.path.append("..")

from text_bot.nlp_model.nlp_model import NlpModel
from text_bot.utils import load_documents

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
    CTDocumentSubsectionTopics,\
    QuotesDocuments


from text_bot.nlp_model.rag.prompt_creator import PromptCreator
from text_bot.nlp_model.mml_model import MmlModel
from text_bot.nlp_model.replicate_model import ReplicateModel
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

class VectorizeDocumentsEngine:


    def __init__(self, nlp_model :NlpModel, mml_model:MmlModel):
        self.model = nlp_model
        self.prompt_creator = PromptCreator(nlp_model, mml_model)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_CHUNK_SIZE, chunk_overlap=MAX_CHUNK_OVERLAP_SIZE)
        self.recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_SEMANTIC_CHUNK_SIZE, chunk_overlap=MAX_SEMANTIC_CHUNK_OVERLAP_SIZE)
        self.pages_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_PAGE_SIZE, chunk_overlap=0)
        self.markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)

        self.replicate_model = ReplicateModel()

        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)


    def load_documents_to_db(self):
        documents = load_documents("documents/")
        for document_pages in documents:

            document_pages_formatted = self.get_document_split_pages(document_pages)
            md_header_splits = self.markdown_splitter.split_text(document_pages_formatted)

            self.replicate_model.do_all_evaluations(md_header_splits)




    def load_documents_to_db_1(self):
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

