from __future__ import absolute_import

import logging
import requests
import json
from celery import shared_task
from text_bot.tasks import add_chat_history_to_top_chats_pool

logger = logging.getLogger(__name__)

@shared_task
def run_add_chat_history_to_top_chats_pool():
    logger.info('run_add_chat_history_to_top_chats_pool execution.')
    add_chat_history_to_top_chats_pool.delay()
