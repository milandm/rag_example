from django.db import models
from pgvector.django import VectorField
from pgvector.django import IvfflatIndex
from pgvector.django import HnswIndex

from text_bot.views.managers import TopChatQuestionsManager,\
                                     UserHistoryManager,\
                                     CTDocumentSplitManager,\
                                     CTDocumentSectionManager,\
                                     CTDocumentSectionTitleManager,\
                                     CTDocumentSectionTextManager,\
                                     CTDocumentSectionReferencesManager,\
                                     CTDocumentSectionTopicsManager,\
                                     CTDocumentSubsectionManager,\
                                     CTDocumentSubsectionTitleManager,\
                                     CTDocumentSubsectionTextManager,\
                                     CTDocumentSubsectionReferencesManager,\
                                     CTDocumentSubsectionTopicsManager


# { input: searchQuery, history_key: historyKey }

class TextbotOutput(models.Model):
    history_key = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']

class UserHistory(models.Model):
    history_key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey('auth.User', related_name='history_keys', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

# multi-qa-distilbert-cos-v1
MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE = 1536
class ChatQuestion(models.Model):

    class Meta:
        indexes = [
            IvfflatIndex(
                name='my_index',
                fields=['embedding'],
                lists=100,
                opclasses=['vector_l2_ops']
            )
        ]

    history_key = models.CharField(max_length=100)
    embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    appearance_count = models.IntegerField()
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TopChatQuestionsManager()

    class Meta:
        ordering = ['-id']

class CTDocument(models.Model):
    class Meta:
        ordering = ['-id']

    # find all main topics/contexts
    # find all splits with main context explained
    document_version = models.IntegerField()
    document_title = models.CharField(max_length=100)
    document_filename = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class CTDocumentPage(models.Model):
    class Meta:
        ordering = ['-id']

    ct_document = models.ForeignKey(CTDocument, on_delete=models.CASCADE, related_name='document_pages')
    document_page_text = models.CharField(max_length=6000)
    document_page_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)



# extract topics, extract keywords, extract possible questions
# Counter Hypothetical Document Embeddings (HyDE)
# CREATE QUESTIONS FOR CONTEXT
class CTDocumentSplit(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            IvfflatIndex(
                name='document_ivf_flat_index',
                fields=['embedding'],
                lists=100,
                # probes = 10,
                opclasses=['vector_cosine_ops']
            ),

            # or
            # HnswIndex(
            #     name='document_hnsw_index',
            #     fields=['embedding'],
            #     m=16,
            #     ef_construction=64,
            #     opclasses=['vector_l2_ops']
            # )
        ]

    # find split with main context
    # find semantically connected splits
    # is this split related to previous split context
    # is next split related to this slit content
    # what is this split related to in bigger context
    # pick up all splits related with bigger context

    # main context split
    # semantically connected splits

    ct_document = models.ForeignKey(CTDocument, on_delete=models.CASCADE, related_name='document_splits')
    document_title = models.CharField(max_length=100)
    document_filename = models.CharField(max_length=100)
    document_page = models.IntegerField()
    split_text = models.CharField(max_length=1500)
    split_text_compression = models.CharField(max_length=1500)
    split_number = models.IntegerField()
    embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSplitManager()


class CTDocumentSection(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            HnswIndex(
                name='section_summary_hnsw_index',
                fields=['content_summary_embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]

    ct_document = models.ForeignKey(CTDocument, on_delete=models.CASCADE, related_name='document_sections')
    document_title = models.CharField(max_length=100)
    document_filename = models.CharField(max_length=100)
    document_page = models.IntegerField()

    section_title_value = models.CharField(max_length=100)
    section_text_value = models.CharField(max_length=1500)
    section_content_summary_value = models.CharField(max_length=1500)
    section_references_value = models.CharField(max_length=1500)
    section_topics_value = models.CharField(max_length=1500)
    section_number = models.IntegerField()

    # 'title_embedding', 'text_embedding', 'content_summary_embedding', 'references_embedding', 'topics_embedding'

    title_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    text_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    content_summary_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    references_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    topics_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSectionManager()

class CTDocumentSectionTitle(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            HnswIndex(
                name='section_title_hnsw_index',
                fields=['title_embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]

    ct_document_section = models.ForeignKey(CTDocumentSection, on_delete=models.CASCADE, related_name='section_title')

    section_title = models.CharField(max_length=100)
    section_text = models.CharField(max_length=1500)
    section_content_summary = models.CharField(max_length=1500)
    section_references = models.CharField(max_length=1500)
    section_topics = models.CharField(max_length=1500)
    section_number = models.IntegerField()

    title_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    text_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    content_summary_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    references_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    topics_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSectionTitleManager()

class CTDocumentSectionText(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            HnswIndex(
                name='section_text_hnsw_index',
                fields=['text_embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]

    ct_document_section = models.ForeignKey(CTDocumentSection, on_delete=models.CASCADE, related_name='section_text')

    section_title = models.CharField(max_length=100)
    section_text = models.CharField(max_length=1500)
    section_content_summary = models.CharField(max_length=1500)
    section_references = models.CharField(max_length=1500)
    section_topics = models.CharField(max_length=1500)
    section_number = models.IntegerField()

    title_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    text_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    content_summary_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    references_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    topics_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSectionTextManager()


class CTDocumentSectionReferences(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            HnswIndex(
                name='section_references_hnsw_index',
                fields=['references_embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]

    ct_document_section = models.ForeignKey(CTDocumentSection, on_delete=models.CASCADE, related_name='section_references')

    section_title = models.CharField(max_length=100)
    section_text = models.CharField(max_length=1500)
    section_content_summary = models.CharField(max_length=1500)
    section_references = models.CharField(max_length=1500)
    section_topics = models.CharField(max_length=1500)
    section_number = models.IntegerField()

    title_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    text_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    content_summary_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    references_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    topics_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSectionReferencesManager()


class CTDocumentSectionTopics(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            HnswIndex(
                name='section_topics_hnsw_index',
                fields=['topics_embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]

    ct_document_section = models.ForeignKey(CTDocumentSection, on_delete=models.CASCADE, related_name='section_topics')

    section_title = models.CharField(max_length=100)
    section_text = models.CharField(max_length=1500)
    section_content_summary = models.CharField(max_length=1500)
    section_references = models.CharField(max_length=1500)
    section_topics = models.CharField(max_length=1500)
    section_number = models.IntegerField()

    # 'title_embedding', 'text_embedding', 'content_summary_embedding', 'references_embedding', 'topics_embedding'

    title_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    text_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    content_summary_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    references_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    topics_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSectionTopicsManager()



class CTDocumentSubsection(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            HnswIndex(
                name='subs_summary_hnsw_index',
                fields=['content_summary_embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]

    ct_document_section = models.ForeignKey(CTDocumentSection, on_delete=models.CASCADE, related_name='section_subsections')

    subsection_title_value = models.CharField(max_length=100)
    subsection_text_value = models.CharField(max_length=1500)
    subsection_content_summary_value = models.CharField(max_length=1500)
    subsection_references_value = models.CharField(max_length=1500)
    subsection_topics_value = models.CharField(max_length=1500)
    subsection_number = models.IntegerField()


    title_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    text_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    content_summary_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    references_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    topics_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSubsectionManager()


class CTDocumentSubsectionTitle(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            HnswIndex(
                name='subs_title_hnsw_index',
                fields=['title_embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]

    ct_document_subsection = models.ForeignKey(CTDocumentSubsection, on_delete=models.CASCADE,
                                            related_name='subsection_title')

    subsection_title = models.CharField(max_length=100)
    subsection_text = models.CharField(max_length=1500)
    subsection_content_summary = models.CharField(max_length=1500)
    subsection_references = models.CharField(max_length=1500)
    subsection_topics = models.CharField(max_length=1500)
    subsection_number = models.IntegerField()

    title_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    text_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    content_summary_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    references_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    topics_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSubsectionTitleManager()

class CTDocumentSubsectionText(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            HnswIndex(
                name='subs_text_hnsw_index',
                fields=['text_embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]

    ct_document_subsection = models.ForeignKey(CTDocumentSubsection, on_delete=models.CASCADE,
                                               related_name='subsection_text')

    subsection_title = models.CharField(max_length=100)
    subsection_text = models.CharField(max_length=1500)
    subsection_content_summary = models.CharField(max_length=1500)
    subsection_references = models.CharField(max_length=1500)
    subsection_topics = models.CharField(max_length=1500)
    subsection_number = models.IntegerField()

    title_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    text_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    content_summary_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    references_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    topics_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSubsectionTextManager()

class CTDocumentSubsectionReferences(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            HnswIndex(
                name='subs_references_hnsw_index',
                fields=['references_embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]

    ct_document_subsection = models.ForeignKey(CTDocumentSubsection, on_delete=models.CASCADE,
                                               related_name='subsection_references')

    subsection_title = models.CharField(max_length=100)
    subsection_text = models.CharField(max_length=1500)
    subsection_content_summary = models.CharField(max_length=1500)
    subsection_references = models.CharField(max_length=1500)
    subsection_topics = models.CharField(max_length=1500)
    subsection_number = models.IntegerField()

    title_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    text_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    content_summary_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    references_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    topics_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSubsectionReferencesManager()


class CTDocumentSubsectionTopics(models.Model):
    class Meta:
        ordering = ['-id']
        indexes = [
            HnswIndex(
                name='subs_topics_hnsw_index',
                fields=['topics_embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]

    ct_document_subsection = models.ForeignKey(CTDocumentSubsection, on_delete=models.CASCADE,
                                               related_name='subsection_topics')

    subsection_title = models.CharField(max_length=100)
    subsection_text = models.CharField(max_length=1500)
    subsection_content_summary = models.CharField(max_length=1500)
    subsection_references = models.CharField(max_length=1500)
    subsection_topics = models.CharField(max_length=1500)
    subsection_number = models.IntegerField()

    title_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    text_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    content_summary_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    references_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)
    topics_embedding = VectorField(dimensions=MULTI_QA_DISTILBERT_COS_V1_VECTOR_SIZE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CTDocumentSubsectionTopicsManager()


# {
#     "Section Title": "I. УВОДНЕ ОДРЕДБЕ",
#     "Section Content Summary": "Introduction to the regulation specifying the content and labeling of external and internal packaging of medicines, additional labeling, and the content of the medicine instructions.",
#     "Section Text": "I. УВОДНЕ ОДРЕДБЕ\nСадржина правилника\nЧлан 1.\nОвим правилником прописује се садржај и начин обележавања спољњег и унутрашњег паковања\nлека, додатно обележавање лека, као и садржај упутства за лек.",
#     "Section References": ["правилник", "лек", "спољње паковање", "унутрашње паковање", "обележавање",
#                            "упутство за лек"],
#     "Section Topics": ["Садржина правилника", "обележавање", "упутство за лек"],
#     "Subsections": [
#         {
#             "Subsection Title": "Садржина правилника",
#             "Subsection Content Summary": "Defines the regulation of the content and labeling of external and internal packaging of medicines, additional labeling, and the content of the medicine instructions.",
#             "Subsection Text": "Члан 1.\nОвим правилником прописује се садржај и начин обележавања спољњег и унутрашњег паковања\nлека, додатно обележавање лека, као и садржај упутства за лек.",
#             "Subsection References": ["правилник", "лек", "спољње паковање", "унутрашње паковање",
#                                       "обележавање", "упутство за лек"],
#             "Subsection Topics": ["правилник", "обележавање", "упутство за лек"]
#         }
#     ]
# }