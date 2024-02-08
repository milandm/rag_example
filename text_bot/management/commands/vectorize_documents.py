from django.core.management.base import BaseCommand
from text_bot.nlp_model.rag.vectorize_documents_engine import VectorizeDocumentsEngine
from text_bot.nlp_model.openai_model import OpenaiModel

class Command(BaseCommand):
    help = "Create mock data for YourModel"

    def handle(self, *args, **kwargs):
        # Your code to create mock data here
        vectorize_documents_engine = VectorizeDocumentsEngine(OpenaiModel())
        vectorize_documents_engine.load_semantic_document_chunks_to_db()
        self.stdout.write(self.style.SUCCESS('Successfully created mock data'))



