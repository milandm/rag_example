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
    CTDocumentSubsectionTopics


from text_bot.nlp_model.rag.prompt_creator import PromptCreator

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
        self.semantic_text_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_SEMANTIC_CHUNK_SIZE, chunk_overlap=MAX_SEMANTIC_CHUNK_OVERLAP_SIZE)
        self.pages_splitter = RecursiveCharacterTextSplitter(chunk_size=MAX_PAGE_SIZE, chunk_overlap=0)
        self.markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)


    def load_documents_to_db(self):
        documents = load_documents("documents/")
        for document_pages in documents:

            document_pages_formatted = self.get_document_split_pages(document_pages)

            md_header_splits = self.markdown_splitter.split_text(document_pages_formatted)
            documents_splits = self.text_splitter.split_documents(md_header_splits)

            self.add_document_page(document_pages_formatted)
            self.add_document_splits(documents_splits)

    def load_semantic_document_chunks_to_db(self):
        documents = load_documents("documents/")
        for document_pages in documents:

            document_page_formatted_list = self.get_document_split_pages(document_pages)

            for document_page_idx, document_page_formatted in enumerate(document_page_formatted_list):
                previous_last_semantic_chunk = ""
                if not self.page_already_added_to_db(document_page_formatted, document_page_idx):
                    documents_splits = self.semantic_text_splitter.split_documents([document_page_formatted])
                    previous_last_semantic_chunk = self.add_semantic_document_splits(documents_splits, previous_last_semantic_chunk, document_page_idx)
                    self.add_document_page(document_page_formatted, document_page_idx)

    def splits_already_added_to_db(self, ct_document, documents_splits):
        old_document_splits_count = ct_document.document_splits.all().count()
        return old_document_splits_count >= len(documents_splits)

    def page_index_already_added_to_db(self, ct_document, documents_page_index):
        old_document_pages_count = ct_document.document_pages.all().count()
        return old_document_pages_count > documents_page_index

    def get_text_compression(self, documents_split_txt):
        text_split_compression = self.prompt_creator.get_document_text_compression(documents_split_txt)
        text_split_compression_check = self.prompt_creator.get_document_text_compression_check(documents_split_txt, text_split_compression)

        if text_split_compression_check and "YES" in text_split_compression_check:
            return text_split_compression
        else:
            return text_split_compression_check


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
            # ct_document.document_pages.all().delete()
            # for i, document_page in enumerate(document_page):
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
                split_text_compression = self.get_text_compression(documents_split.page_content)

                print("Document title: ", ct_document.document_title)
                print("Document filename: ", ct_document.document_filename)
                print("Document page: ", document_page)
                print("Split text: ", split_text)
                print("Split text compression: ", split_text_compression)

                embedding = self.model.get_embedding(split_text)

                CTDocumentSplit.objects.create(
                    ct_document=ct_document,
                    document_title=ct_document.document_title,
                    document_filename=ct_document.document_filename,
                    document_page=document_page,
                    split_text=split_text,
                    split_text_compression=split_text_compression,
                    split_number=i,
                    embedding=embedding)

    def add_semantic_document_splits(self, documents_splits, previous_last_semantic_chunk = "", document_page_idx = 0):
        ct_document = self.get_document(documents_splits[0])

        ct_document.document_sections.filter(document_page=document_page_idx).all().delete()

        section_index = 0

        for i, documents_split in enumerate(documents_splits):
            # document_page = documents_split.metadata.get("page", 0)
            split_text = documents_split.page_content

            semantic_sections_json_list = self.prompt_creator.get_document_semantic_text_chunks(split_text,
                                                                                              previous_last_semantic_chunk)

            if not semantic_sections_json_list or not isinstance(semantic_sections_json_list, list):
                continue

            previous_last_subsections_list = semantic_sections_json_list[-1].get("subsection_list", [])
            if previous_last_subsections_list:
                previous_last_semantic_chunk = previous_last_subsections_list[-1].get("subsection_text", "")

            for i, raw_semantic_section_json in enumerate(semantic_sections_json_list):
                print("semantic_section_json: ", str(raw_semantic_section_json))

                semantic_subsections_json_list = raw_semantic_section_json.get("subsection_list",[])

                semantic_section_json = self.prepare_semantic_section_json(raw_semantic_section_json, section_index)
                ct_document_section = CTDocumentSection.objects.create_from_json(semantic_section_json, ct_document, document_page_idx)
                ct_document_section_title = CTDocumentSectionTitle.objects.create_from_json(semantic_section_json, ct_document_section)
                ct_document_section_text = CTDocumentSectionText.objects.create_from_json(semantic_section_json, ct_document_section)
                ct_document_section_references = CTDocumentSectionReferences.objects.create_from_json(semantic_section_json, ct_document_section)
                ct_document_section_topics = CTDocumentSectionTopics.objects.create_from_json(semantic_section_json, ct_document_section)

                for j, raw_semantic_subsection_json in enumerate(semantic_subsections_json_list):

                    semantic_subsection_json = self.prepare_semantic_subsection_json(raw_semantic_subsection_json, j)
                    ct_document_subsection = CTDocumentSubsection.objects.create_from_json(semantic_subsection_json, ct_document_section)
                    ct_document_subsection_title = CTDocumentSubsectionTitle.objects.create_from_json(semantic_subsection_json, ct_document_subsection)
                    ct_document_subsection_text = CTDocumentSubsectionText.objects.create_from_json(semantic_subsection_json, ct_document_subsection)
                    ct_document_subsection_references = CTDocumentSubsectionReferences.objects.create_from_json(semantic_subsection_json, ct_document_subsection)
                    ct_document_subsection_topics = CTDocumentSubsectionTopics.objects.create_from_json(semantic_subsection_json, ct_document_subsection)

                section_index+=1

        return previous_last_semantic_chunk


    def prepare_semantic_section_json(self, semantic_section_json, section_idx):

        section_title = semantic_section_json.get("section_title","")
        section_text = semantic_section_json.get("section_text","")
        section_content_summary = semantic_section_json.get("section_content_summary","")

        section_references = semantic_section_json.get("section_references","")
        section_references_join = ','.join(section_references)

        section_topics = semantic_section_json.get("section_topics","")
        section_topics_join = ','.join(section_topics)

        section_number = section_idx
        semantic_section_json["section_number"] = section_number


        title_embedding = self.model.get_embedding(section_title)
        semantic_section_json["title_embedding"] = title_embedding

        text_embedding = self.model.get_embedding(section_text)
        semantic_section_json["text_embedding"] = text_embedding

        content_summary_embedding = self.model.get_embedding(section_content_summary)
        semantic_section_json["content_summary_embedding"] = content_summary_embedding

        references_embedding = self.model.get_embedding(section_references_join)
        semantic_section_json["references_embedding"] = references_embedding

        topics_embedding = self.model.get_embedding(section_topics_join)
        semantic_section_json["topics_embedding"] = topics_embedding

        return semantic_section_json


    def prepare_semantic_subsection_json(self, semantic_subsection_json, subsection_idx):

        subsection_title = semantic_subsection_json.get("subsection_title", "")
        subsection_text = semantic_subsection_json.get("subsection_text", "")
        subsection_content_summary = semantic_subsection_json.get("subsection_content_summary", "")

        subsection_references = semantic_subsection_json.get("subsection_references", "")
        subsection_references_join = ','.join(subsection_references)

        subsection_topics = semantic_subsection_json.get("subsection_topics", "")
        subsection_topics_join = ','.join(subsection_topics)

        subsection_number = subsection_idx
        semantic_subsection_json["subsection_number"] = subsection_number


        subsection_title_embedding = self.model.get_embedding(subsection_title)
        semantic_subsection_json["subsection_title_embedding"] = subsection_title_embedding

        subsection_text_embedding = self.model.get_embedding(subsection_text)
        semantic_subsection_json["subsection_text_embedding"] = subsection_text_embedding

        subsection_content_summary_embedding = self.model.get_embedding(subsection_content_summary)
        semantic_subsection_json["subsection_content_summary_embedding"] = subsection_content_summary_embedding

        subsection_references_embedding = self.model.get_embedding(subsection_references_join)
        semantic_subsection_json["subsection_references_embedding"] = subsection_references_embedding

        subsection_topics_embedding = self.model.get_embedding(subsection_topics_join)
        semantic_subsection_json["subsection_topics_embedding"] = subsection_topics_embedding

        return semantic_subsection_json
