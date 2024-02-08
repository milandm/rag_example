from django.core.management.base import BaseCommand
from text_bot.nlp_model.text_extraction.extractor_vectorize_documents_engine import ExtractorVectorizeDocumentsEngine
from text_bot.nlp_model.llama_model import LLamaModel

class Command(BaseCommand):
    help = "Create mock data for YourModel"

    def handle(self, *args, **kwargs):
        # Your code to create mock data here
        vectorize_documents_engine = ExtractorVectorizeDocumentsEngine(LLamaModel())
        vectorize_documents_engine.load_semantic_document_chunks_to_db("documents_protocol/protocol_amendment31082023.pdf")
        self.stdout.write(self.style.SUCCESS('Successfully created mock data'))



