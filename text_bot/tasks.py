from celery import shared_task
from text_bot.views.models import ChatQuestion, UserHistory
from text_bot.utils import extract_human_ai_conversation_from_string, get_base64_string, get_questions_list_from_text_bot_api_buffer, get_questions_list_from_text_bot_api_structured_buffer
from api_crud.settings import REACT_APP_TAX3PO_API_DEV_URL, REACT_APP_TAX3PO_API_KEY, TAX3PO_API_ENDPOINT_CONVERSATION
import requests
import logging

logger = logging.getLogger(__name__)

@shared_task
def add_chat_history_to_top_chats_pool():
    logger.info('add_chat_history_to_top_chats_pool execution.')
    conversation_history_list = UserHistory.objects.all()
    for conversation_history in conversation_history_list:
        history_response_buffer = get_chat_response(conversation_history.history_key)
        conversation_questions_list = get_questions_list_from_text_bot_api_buffer(history_response_buffer)
        for conversation_question in conversation_questions_list:
            ChatQuestion.objects.add_chat_question_to_top_chat_pool(conversation_question, conversation_history.history_key)


def get_chat_response(history_key):

    input = " "

    base64_string = get_base64_string(REACT_APP_TAX3PO_API_KEY)

    headers = {'Authorization': "Basic " + base64_string,
               'Content-Type': 'application/x-www-form-urlencoded'}

    data = {'input': input, 'history_key': history_key}

    response = requests.post(REACT_APP_TAX3PO_API_DEV_URL+TAX3PO_API_ENDPOINT_CONVERSATION, headers=headers, data=data)
    # You may want to check that the request was successful
    if response.status_code == 200:
        data = response.json()  # parse JSON response into a Python dictionary
        return data['buffer']
    else:
        return ""



