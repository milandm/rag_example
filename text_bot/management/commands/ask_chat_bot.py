from django.core.management.base import BaseCommand
from text_bot.nlp_model.rag.chat_manager import ChatManager
from text_bot.nlp_model.openai_model import OpenaiModel

class Command(BaseCommand):
    help = "Create mock data for YourModel"

    def handle(self, *args, **kwargs):
        # Your code to create mock data here
        chat_manager = ChatManager(OpenaiModel())
        current_query = "Koji su koraci neophodni da bi se izvrsilo klinicko istrazivanje u Srbiji?"
        chat_manager.send_user_query(current_query)
        self.stdout.write(self.style.SUCCESS('Successfully created mock data'))



