import re
import base64
import json
import os
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from pathlib import Path
import time
import functools


def load_file_content(file_path):
    """
    Load the content of the given file path as a string.

    :param file_path: The full path to the file to be read.
    :return: A string containing the contents of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except OSError as e:
        print(f"An error occurred: {e}")
        return None


def get_file_paths(directory, extensions=('.cbl', '.cob', '.cpy')):
    """
    Get a list of full file paths for all COBOL-related files in a project directory.

    :param directory: The path to the root directory of the COBOL project.
    :param extensions: A tuple of file extensions to include (defaults to .cbl, .cob, .cpy).
    :return: A list of full paths to the COBOL files.
    """
    cobol_file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                full_path = os.path.join(root, file)
                cobol_file_paths.append(full_path)
    return cobol_file_paths


def load_files_contents(self, project_root_path):
    cobol_files_contents = []
    # Walk through the directory
    for root, dirs, files in os.walk(project_root_path):
        for file in files:
            if file.lower().endswith('.cbl') or file.lower().endswith('.cob'):  # Check for .cbl or .cob files
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as cobol_file:
                    contents = cobol_file.read()
                    cobol_files_contents.append(contents)
                    print(f'Loaded COBOL file: {full_path}')
    return cobol_files_contents

def retry(max_retries=3, initial_delay=1, backoff=2, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = max_retries
            delay = initial_delay
            while retries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    time.sleep(delay)
                    delay *= backoff
                    retries -= 1
            return func(*args, **kwargs)  # Last attempt
        return wrapper
    return decorator

def extract_json_data(input_string):
    # Regular expression pattern to extract JSON data
    json_pattern = r'```json\s*\n(\[.*?\])\s*\n```'

    # Search for the JSON string using the regular expression
    match = re.search(json_pattern, input_string, re.DOTALL)

    if match:
        # Extract the JSON string
        json_string = match.group(1)

        # Parse the JSON string into a Python object
        json_data = json.loads(json_string)

def extract_clean_json_data(input_string):
    # Regular expression to find JSON structure
    json_pattern = r"```json(.+?)```"

    # Search for JSON in the given text
    match = re.search(json_pattern, input_string, re.DOTALL)

    if match:
        json_text = match.group(1).strip()  # Remove extra spaces or newlines
        try:
            # Parse the extracted text to validate and format as JSON
            parsed_json = json.loads(json_text)
            # return json.dumps(parsed_json, indent=4, ensure_ascii=False)
            return parsed_json
        except json.JSONDecodeError as e:
            return f"Error parsing JSON: {e}"
    else:
        return "No JSON found in the text"



def remove_quotes(s):
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s

def extract_single_value_openai_content(openai_response_content: str, extract_key: str):
    # Define a pattern and find match
    value = openai_response_content.replace(extract_key,"")
    return value


def parse_openai_response(openai_response):
    openai_response = json.loads(openai_response)
    openai_response.get("choices")[0].get("message").get("content")
# {
#   "id": "chatcmpl-898dSJDcr3PPCtfcX3FA8WHU8o6hy",
#   "object": "chat.completion",
#   "created": 1697188838,
#   "model": "gpt-3.5-turbo-0613",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": "TITLE: Uputstvo za popunjavanje kvartalnog izve\u0161taja o toku sprovo\u0111enja klini\u010dkog ispitivanja"
#       },
#       "finish_reason": "stop"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 446,
#     "completion_tokens": 38,
#     "total_tokens": 484
#   }
# }



def get_base64_string(string_key):
    bytes_s = string_key.encode('utf-8')
    base64_bytes = base64.b64encode(bytes_s)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

def extract_human_ai_conversation_from_string(text):
    if not text:
        return []

    text = text.strip()
    text = f"\n{text}"
    print(text)
    # Split into separate 'Human' and 'AI' messages based on '\nHuman: ' or '\nAI: '
    human_messages = re.split('\nHuman:', text)

    # For each 'Human' message, further split into 'Human' and 'AI' parts
    parsed_messages = []
    for human_message in human_messages:
        parts = re.split('\nAI:', human_message)
        human_text = parts[0].replace('Human: ', '').strip()
        if human_text and len(human_text) > 0:
            parsed_messages.append({'type': 'HumanMessage', 'text': human_text})
        if len(parts) > 1:
            ai_text = parts[1].replace('AI: ', '').strip()
            if ai_text and len(ai_text) > 0:
                parsed_messages.append({'type': 'AIMessage', 'text': f'ANSWER: \n- {ai_text}'})

    return parsed_messages


def get_questions_list_from_text_bot_api_buffer(text):
    if not text:
        return []

    text = text.strip()
    text = f"\n{text}"
    print(text)
    # Split into separate 'Human' and 'AI' messages based on '\nHuman: ' or '\nAI: '
    human_messages = re.split('\nHuman:', text)

    # For each 'Human' message, further split into 'Human' and 'AI' parts
    parsed_messages = []
    for human_message in human_messages:
        parts = re.split('\nAI:', human_message)
        human_text = parts[0].replace('Human: ', '').strip()
        if human_text and len(human_text) > 0:
            parsed_messages.append(human_text)
    return parsed_messages

def get_questions_list_from_text_bot_api_structured_buffer(history_response_buffer):
    if not history_response_buffer:
        return []

    # For each 'Human' message, further split into 'Human' and 'AI' parts
    parsed_messages = []
    for human_message in history_response_buffer:
        if human_message['type'] == 'HumanMessage':
            parsed_messages.append(human_message['text'])
    return parsed_messages


@staticmethod
def load_file(file_name: str):
    with open(file_name, "r") as file:
        meditations_json = json.load(file)
        return meditations_json

def get_proper_file_loader(file_path):
    print("get_proper_file_loader "+ str(file_path))
    loader = None
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx') or file_path.endswith('.doc'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    return loader

def load_document(documents_path):
    file_name = os.path.basename(documents_path)
    all_document_pages = list()
    try:
        loader = get_proper_file_loader(documents_path)
        if loader:
            document_pages = loader.load()
            for page in document_pages:
                page.metadata["source"] = file_name
            # print("document: "+str(document))
            # print("filename: "+str(file.name))
            all_document_pages.extend(document_pages)
    except Exception as e:
        print(e)
    return all_document_pages

def load_documents(documents_folder_path):
    documents = list()
    for file_path in os.listdir(documents_folder_path):
        file = Path(file_path)
        base_path = os.path.dirname(file.absolute())
        try:
            loader = get_proper_file_loader(base_path+"/"+documents_folder_path+file.name)
            if loader:
                document_pages = loader.load()
                for page in document_pages:
                    page.metadata["source"] = file.name
                # print("document: "+str(document))
                # print("filename: "+str(file.name))
                documents.append(document_pages)
        except Exception as e:
            print(e)
    return documents


def get_related_objects(instance):
    related_objects = {}

    # Loop through all fields of the instance's model
    for field in instance._meta.get_fields():

        # If the field is a reverse relation from another model
        if (field.one_to_many or field.one_to_one) and field.auto_created and not field.concrete:
            # Use `getattr` to fetch the related object(s)
            related_name = field.get_accessor_name()
            related_obj = getattr(instance, related_name)

            # If it's a OneToOneField or ForeignKey, it won't have 'all()' method
            if field.one_to_many:
                related_objects[related_name] = related_obj.all()
            else:
                related_objects[related_name] = related_obj

    return related_objects
