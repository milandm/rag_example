from django.core.management.base import BaseCommand
from text_bot.nlp_model.cobol_project_rag.vectorize_cobol_code_engine import VectorizeCobolCodeEngine
from text_bot.nlp_model.openai_model import OpenaiModel

class Command(BaseCommand):
    help = "Create mock data for YourModel"

    def handle(self, *args, **kwargs):
        # Your code to create mock data here
        vectorize_documents_engine = VectorizeCobolCodeEngine(OpenaiModel())
        vectorize_documents_engine.load_cobol_project_files("cobol_project_code/")
        self.stdout.write(self.style.SUCCESS('Successfully created mock data'))