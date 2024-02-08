from django.core.management.base import BaseCommand
from text_bot.tasks import add_chat_history_to_top_chats_pool

class Command(BaseCommand):
    help = 'Run my task from command line'

    def handle(self, *args, **kwargs):
        add_chat_history_to_top_chats_pool.delay()