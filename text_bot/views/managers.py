from django.db import models
from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance, L2Distance
from text_bot.ai_utils import get_distance_scores, check_distance_scores_out

class TopChatQuestionsManager(models.Manager):

    def add_chat_question_to_top_chat_pool(self, question_text: str, history_key:str):
        # paraphrase-multilingual-mpnet-base-v2 Dimensions:	768
        # multi-qa-distilbert-cos-v1 Dimensions: 768
        # dimension all-MiniLM-L12-v2 Dimensions: 384

        model = SentenceTransformer('multi-qa-distilbert-cos-v1')
        question_embedding = model.encode([question_text], normalize_embeddings=True).tolist()[0]

        # add_new_anchor_db(dataset_groups[16]['text'], groups_sentences_embeddings[16])
        sentence_rows_list = self.query_embedding_in_db(question_embedding)
        sentence_to_update_list = list()
        is_similar_to_existing = False
        if sentence_rows_list:
            for sentence in sentence_rows_list:
                distance_scores = get_distance_scores(question_embedding, sentence.embedding)
                if not check_distance_scores_out(distance_scores):
                    is_similar_to_existing = True
                    sentence_to_update_list.append({"sentence": sentence, "distance_scores": distance_scores})

        if is_similar_to_existing:
            if sentence_to_update_list:
                sentence_to_update = \
                max(sentence_to_update_list, key=lambda x: x["distance_scores"]['cosine_scores'])["sentence"]
                self.update_group_count_db(sentence_to_update)
        else:
            self.add_new_anchor_db(question_text, question_embedding, history_key)

    def add_new_anchor_db(self, question_text, question_embedding, history_key):
        self.create(history_key = history_key,
                    text=question_text,
                    embedding=question_embedding,
                    appearance_count=1)

    def query_embedding_in_db(self, embedding):
        return self.order_by(L2Distance('embedding', embedding))[:5]

    def update_group_count_db(self, chat_question):
        chat_question.appearance_count = chat_question.appearance_count+1
        chat_question.save()

class UserHistoryManager(models.Manager):

    def get_user_history(self, user_id):
        return self.filter(creator=user_id)


# COSINE_DISTANCE_TRESHOLD = 0.15
COSINE_DISTANCE_TRESHOLD = 0.2
# COSINE_DISTANCE_TRESHOLD = 0.5
# COSINE_DISTANCE_QUERY = cosine_distance__lt
# COSINE_DISTANCE_QUERY = cosine_distance__gt
# COSINE_DISTANCE_TYPE = cosine_distance



class CTDocumentSplitManager(models.Manager):



    # def add_document_embedding_db(self, document_title, document_text, document_embedding):
    #     self.create(document_title = document_title,
    #                 text=document_text,
    #                 embedding=document_embedding)

    def query_embedding_in_db(self, embedding):
        return self.order_by(CosineDistance('embedding', embedding)).all()[:20]

    def query_embedding_and_filter_out_in_db(self, document_title, embedding):
        items = self.filter(document_title=document_title).order_by(CosineDistance('embedding', embedding))[:5]
        return items

    def query_embedding_by_distance(self, embedding):
        return self.alias(cosine_distance=CosineDistance('embedding', embedding))\
            .filter(cosine_distance__lt=COSINE_DISTANCE_TRESHOLD).order_by('cosine_distance')



class CTDocumentSectionManager(models.Manager):

    # [{
    #     "section_title": "",
    #     "section_content_summary": "",
    #     "section_text": "",
    #     "section_references": [],
    #     "section_topics": [],
    #     "subsection_list":
    #         [
    #             {
    #                 "subsection_title": "",
    #                 "subsection_content_summary": "",
    #                 "subsection_text": "",
    #                 "subsection_references": [],
    #                 "subsection_topics": []
    #             }
    #         ]
    # }]
    # """

    def create_from_json(self, semantic_section_json, ct_document, document_page_idx):

        section_title = semantic_section_json.get("section_title", "")
        section_text = semantic_section_json.get("section_text", "")
        section_content_summary = semantic_section_json.get("section_content_summary", "")
        section_references = semantic_section_json.get("section_references", "")
        section_topics = semantic_section_json.get("section_topics", "")
        section_number = semantic_section_json["section_number"]
        title_embedding = semantic_section_json["title_embedding"]
        text_embedding = semantic_section_json["text_embedding"]
        content_summary_embedding = semantic_section_json["content_summary_embedding"]
        references_embedding = semantic_section_json["references_embedding"]
        topics_embedding = semantic_section_json["topics_embedding"]

        ct_document_section = self.create(
            ct_document=ct_document,
            document_title=ct_document.document_title,
            document_filename=ct_document.document_filename,
            document_page=document_page_idx,
            section_title_value = section_title,
            section_text_value = section_text,
            section_content_summary_value = section_content_summary,
            section_references_value = section_references,
            section_topics_value = section_topics,
            section_number = section_number,
            title_embedding = title_embedding,
            text_embedding = text_embedding,
            content_summary_embedding = content_summary_embedding,
            references_embedding = references_embedding,
            topics_embedding = topics_embedding)

        return ct_document_section

    def query_embedding_in_db(self, embedding):
        return self.order_by(CosineDistance('content_summary_embedding', embedding)).all()[:20]

    def query_embedding_by_distance(self, embedding):
        cosine_distance=CosineDistance('content_summary_embedding', embedding)
        return self.annotate(cosine_distance=cosine_distance)\
            .filter(cosine_distance__lt=COSINE_DISTANCE_TRESHOLD)
        # return self.alias(cosine_distance=cosine_distance)\
        #     .filter(cosine_distance=COSINE_DISTANCE_TRESHOLD).order_by('cosine_distance')


class CTDocumentSectionTitleManager(models.Manager):

    def create_from_json(self, semantic_section_json, ct_document_section):

        section_title = semantic_section_json.get("section_title", "")
        section_text = semantic_section_json.get("section_text", "")
        section_content_summary = semantic_section_json.get("section_content_summary", "")
        section_references = semantic_section_json.get("section_references", "")
        section_topics = semantic_section_json.get("section_topics", "")
        section_number = semantic_section_json["section_number"]
        title_embedding = semantic_section_json["title_embedding"]
        text_embedding = semantic_section_json["text_embedding"]
        content_summary_embedding = semantic_section_json["content_summary_embedding"]
        references_embedding = semantic_section_json["references_embedding"]
        topics_embedding = semantic_section_json["topics_embedding"]

        ct_document_section = self.create(
            ct_document_section=ct_document_section,
            section_title=section_title,
            section_text=section_text,
            section_content_summary=section_content_summary,
            section_references=section_references,
            section_topics=section_topics,
            section_number=section_number,
            title_embedding=title_embedding,
            text_embedding=text_embedding,
            content_summary_embedding=content_summary_embedding,
            references_embedding=references_embedding,
            topics_embedding=topics_embedding)

        return ct_document_section


class CTDocumentSectionTextManager(models.Manager):

    def create_from_json(self, semantic_section_json, ct_document_section):

        section_title = semantic_section_json.get("section_title", "")
        section_text = semantic_section_json.get("section_text", "")
        section_content_summary = semantic_section_json.get("section_content_summary", "")
        section_references = semantic_section_json.get("section_references", "")
        section_topics = semantic_section_json.get("section_topics", "")
        section_number = semantic_section_json["section_number"]
        title_embedding = semantic_section_json["title_embedding"]
        text_embedding = semantic_section_json["text_embedding"]
        content_summary_embedding = semantic_section_json["content_summary_embedding"]
        references_embedding = semantic_section_json["references_embedding"]
        topics_embedding = semantic_section_json["topics_embedding"]

        ct_document_section = self.create(
            ct_document_section=ct_document_section,
            section_title=section_title,
            section_text=section_text,
            section_content_summary=section_content_summary,
            section_references=section_references,
            section_topics=section_topics,
            section_number=section_number,
            title_embedding=title_embedding,
            text_embedding=text_embedding,
            content_summary_embedding=content_summary_embedding,
            references_embedding=references_embedding,
            topics_embedding=topics_embedding)

        return ct_document_section

    def query_embedding_in_db(self, embedding):
        return self.order_by(CosineDistance('text_embedding', embedding)).all()[:20]

    def query_embedding_by_distance(self, embedding):
        cosine_distance=CosineDistance('text_embedding', embedding)
        return self.annotate(cosine_distance=cosine_distance)\
            .filter(cosine_distance__lt=COSINE_DISTANCE_TRESHOLD)
        # return self.alias(distance=CosineDistance('text_embedding', embedding))\
        #     .filter(cosine_distance=COSINE_DISTANCE_TRESHOLD).order_by('distance')


class CTDocumentSectionReferencesManager(models.Manager):

    def create_from_json(self, semantic_section_json, ct_document_section):

        section_title = semantic_section_json.get("section_title", "")
        section_text = semantic_section_json.get("section_text", "")
        section_content_summary = semantic_section_json.get("section_content_summary", "")
        section_references = semantic_section_json.get("section_references", "")
        section_topics = semantic_section_json.get("section_topics", "")
        section_number = semantic_section_json["section_number"]
        title_embedding = semantic_section_json["title_embedding"]
        text_embedding = semantic_section_json["text_embedding"]
        content_summary_embedding = semantic_section_json["content_summary_embedding"]
        references_embedding = semantic_section_json["references_embedding"]
        topics_embedding = semantic_section_json["topics_embedding"]

        ct_document_section = self.create(
            ct_document_section=ct_document_section,
            section_title=section_title,
            section_text=section_text,
            section_content_summary=section_content_summary,
            section_references=section_references,
            section_topics=section_topics,
            section_number=section_number,
            title_embedding=title_embedding,
            text_embedding=text_embedding,
            content_summary_embedding=content_summary_embedding,
            references_embedding=references_embedding,
            topics_embedding=topics_embedding)

        return ct_document_section


class CTDocumentSectionTopicsManager(models.Manager):

    def create_from_json(self, semantic_section_json, ct_document_section):

        section_title = semantic_section_json.get("section_title", "")
        section_text = semantic_section_json.get("section_text", "")
        section_content_summary = semantic_section_json.get("section_content_summary", "")
        section_references = semantic_section_json.get("section_references", "")
        section_topics = semantic_section_json.get("section_topics", "")
        section_number = semantic_section_json["section_number"]
        title_embedding = semantic_section_json["title_embedding"]
        text_embedding = semantic_section_json["text_embedding"]
        content_summary_embedding = semantic_section_json["content_summary_embedding"]
        references_embedding = semantic_section_json["references_embedding"]
        topics_embedding = semantic_section_json["topics_embedding"]

        ct_document_section = self.create(
            ct_document_section=ct_document_section,
            section_title=section_title,
            section_text=section_text,
            section_content_summary=section_content_summary,
            section_references=section_references,
            section_topics=section_topics,
            section_number=section_number,
            title_embedding=title_embedding,
            text_embedding=text_embedding,
            content_summary_embedding=content_summary_embedding,
            references_embedding=references_embedding,
            topics_embedding=topics_embedding)

        return ct_document_section


class CTDocumentSubsectionManager(models.Manager):

    def create_from_json(self, semantic_subsection_json, ct_document_section):

        subsection_title = semantic_subsection_json.get("subsection_title", "")
        subsection_text = semantic_subsection_json.get("subsection_text", "")
        subsection_content_summary = semantic_subsection_json.get("subsection_content_summary", "")
        subsection_references = semantic_subsection_json.get("subsection_references", "")
        subsection_topics = semantic_subsection_json.get("subsection_topics", "")
        subsection_number = semantic_subsection_json["subsection_number"]
        subsection_title_embedding = semantic_subsection_json["subsection_title_embedding"]
        subsection_text_embedding = semantic_subsection_json["subsection_text_embedding"]
        subsection_content_summary_embedding = semantic_subsection_json["subsection_content_summary_embedding"]
        subsection_references_embedding = semantic_subsection_json["subsection_references_embedding"]
        subsection_topics_embedding = semantic_subsection_json["subsection_topics_embedding"]

        ct_document_subsection = self.create(
            ct_document_section=ct_document_section,
            subsection_title_value=subsection_title,
            subsection_text_value=subsection_text,
            subsection_content_summary_value=subsection_content_summary,
            subsection_references_value=subsection_references,
            subsection_topics_value=subsection_topics,
            subsection_number=subsection_number,
            title_embedding=subsection_title_embedding,
            text_embedding=subsection_text_embedding,
            content_summary_embedding=subsection_content_summary_embedding,
            references_embedding=subsection_references_embedding,
            topics_embedding=subsection_topics_embedding)

        return ct_document_subsection

    def query_embedding_in_db(self, embedding):
        return self.order_by(CosineDistance('content_summary_embedding', embedding)).all()[:20]

    def query_embedding_by_distance(self, embedding):
        cosine_distance=CosineDistance('content_summary_embedding', embedding)
        return self.annotate(cosine_distance=cosine_distance)\
            .filter(cosine_distance__lt=COSINE_DISTANCE_TRESHOLD)
        # return self.alias(distance=CosineDistance('content_summary_embedding', embedding))\
        #     .filter(cosine_distance=COSINE_DISTANCE_TRESHOLD).order_by('distance')


class CTDocumentSubsectionTitleManager(models.Manager):

    def create_from_json(self, semantic_subsection_json, ct_document_subsection):

        subsection_title = semantic_subsection_json.get("subsection_title", "")
        subsection_text = semantic_subsection_json.get("subsection_text", "")
        subsection_content_summary = semantic_subsection_json.get("subsection_content_summary", "")
        subsection_references = semantic_subsection_json.get("subsection_references", "")
        subsection_topics = semantic_subsection_json.get("subsection_topics", "")
        subsection_number = semantic_subsection_json["subsection_number"]
        subsection_title_embedding = semantic_subsection_json["subsection_title_embedding"]
        subsection_text_embedding = semantic_subsection_json["subsection_text_embedding"]
        subsection_content_summary_embedding = semantic_subsection_json["subsection_content_summary_embedding"]
        subsection_references_embedding = semantic_subsection_json["subsection_references_embedding"]
        subsection_topics_embedding = semantic_subsection_json["subsection_topics_embedding"]

        ct_document_subsection = self.create(
            ct_document_subsection=ct_document_subsection,
            subsection_title=subsection_title,
            subsection_text=subsection_text,
            subsection_content_summary=subsection_content_summary,
            subsection_references=subsection_references,
            subsection_topics=subsection_topics,
            subsection_number=subsection_number,
            title_embedding=subsection_title_embedding,
            text_embedding=subsection_text_embedding,
            content_summary_embedding=subsection_content_summary_embedding,
            references_embedding=subsection_references_embedding,
            topics_embedding=subsection_topics_embedding)

        return ct_document_subsection


class CTDocumentSubsectionTextManager(models.Manager):

    def create_from_json(self, semantic_subsection_json, ct_document_subsection):
        subsection_title = semantic_subsection_json.get("subsection_title", "")
        subsection_text = semantic_subsection_json.get("subsection_text", "")
        subsection_content_summary = semantic_subsection_json.get("subsection_content_summary", "")
        subsection_references = semantic_subsection_json.get("subsection_references", "")
        subsection_topics = semantic_subsection_json.get("subsection_topics", "")
        subsection_number = semantic_subsection_json["subsection_number"]
        subsection_title_embedding = semantic_subsection_json["subsection_title_embedding"]
        subsection_text_embedding = semantic_subsection_json["subsection_text_embedding"]
        subsection_content_summary_embedding = semantic_subsection_json["subsection_content_summary_embedding"]
        subsection_references_embedding = semantic_subsection_json["subsection_references_embedding"]
        subsection_topics_embedding = semantic_subsection_json["subsection_topics_embedding"]

        ct_document_subsection = self.create(
            ct_document_subsection=ct_document_subsection,
            subsection_title=subsection_title,
            subsection_text=subsection_text,
            subsection_content_summary=subsection_content_summary,
            subsection_references=subsection_references,
            subsection_topics=subsection_topics,
            subsection_number=subsection_number,
            title_embedding=subsection_title_embedding,
            text_embedding=subsection_text_embedding,
            content_summary_embedding=subsection_content_summary_embedding,
            references_embedding=subsection_references_embedding,
            topics_embedding=subsection_topics_embedding)

        return ct_document_subsection

    def query_embedding_in_db(self, embedding):
        return self.order_by(CosineDistance('text_embedding', embedding)).all()[:20]

    def query_embedding_by_distance(self, embedding):
        cosine_distance=CosineDistance('text_embedding', embedding)
        return self.annotate(cosine_distance=cosine_distance)\
            .filter(cosine_distance__lt=COSINE_DISTANCE_TRESHOLD)
        # return self.alias(distance=CosineDistance('text_embedding', embedding))\
        #     .filter(cosine_distance=COSINE_DISTANCE_TRESHOLD).order_by('distance')


class CTDocumentSubsectionReferencesManager(models.Manager):

    def create_from_json(self, semantic_subsection_json, ct_document_subsection):
        subsection_title = semantic_subsection_json.get("subsection_title", "")
        subsection_text = semantic_subsection_json.get("subsection_text", "")
        subsection_content_summary = semantic_subsection_json.get("subsection_content_summary", "")
        subsection_references = semantic_subsection_json.get("subsection_references", "")
        subsection_topics = semantic_subsection_json.get("subsection_topics", "")
        subsection_number = semantic_subsection_json["subsection_number"]
        subsection_title_embedding = semantic_subsection_json["subsection_title_embedding"]
        subsection_text_embedding = semantic_subsection_json["subsection_text_embedding"]
        subsection_content_summary_embedding = semantic_subsection_json["subsection_content_summary_embedding"]
        subsection_references_embedding = semantic_subsection_json["subsection_references_embedding"]
        subsection_topics_embedding = semantic_subsection_json["subsection_topics_embedding"]

        ct_document_subsection = self.create(
            ct_document_subsection=ct_document_subsection,
            subsection_title=subsection_title,
            subsection_text=subsection_text,
            subsection_content_summary=subsection_content_summary,
            subsection_references=subsection_references,
            subsection_topics=subsection_topics,
            subsection_number=subsection_number,
            title_embedding=subsection_title_embedding,
            text_embedding=subsection_text_embedding,
            content_summary_embedding=subsection_content_summary_embedding,
            references_embedding=subsection_references_embedding,
            topics_embedding=subsection_topics_embedding)

        return ct_document_subsection


class CTDocumentSubsectionTopicsManager(models.Manager):

    def create_from_json(self, semantic_subsection_json, ct_document_subsection):
        subsection_title = semantic_subsection_json.get("subsection_title", "")
        subsection_text = semantic_subsection_json.get("subsection_text", "")
        subsection_content_summary = semantic_subsection_json.get("subsection_content_summary", "")
        subsection_references = semantic_subsection_json.get("subsection_references", "")
        subsection_topics = semantic_subsection_json.get("subsection_topics", "")
        subsection_number = semantic_subsection_json["subsection_number"]
        subsection_title_embedding = semantic_subsection_json["subsection_title_embedding"]
        subsection_text_embedding = semantic_subsection_json["subsection_text_embedding"]
        subsection_content_summary_embedding = semantic_subsection_json["subsection_content_summary_embedding"]
        subsection_references_embedding = semantic_subsection_json["subsection_references_embedding"]
        subsection_topics_embedding = semantic_subsection_json["subsection_topics_embedding"]

        ct_document_subsection = self.create(
            ct_document_subsection=ct_document_subsection,
            subsection_title=subsection_title,
            subsection_text=subsection_text,
            subsection_content_summary=subsection_content_summary,
            subsection_references=subsection_references,
            subsection_topics=subsection_topics,
            subsection_number=subsection_number,
            title_embedding=subsection_title_embedding,
            text_embedding=subsection_text_embedding,
            content_summary_embedding=subsection_content_summary_embedding,
            references_embedding=subsection_references_embedding,
            topics_embedding=subsection_topics_embedding)

        return ct_document_subsection