import numpy as np


def map_di_words_to_fields(di_words_confidence_list, structured_output):

    di_words_confidence_list = get_di_words_with_offsets(di_words_confidence_list)
    concatenated_text = ' '.join(word_confidence['word_content'] for word_confidence in di_words_confidence_list)
    structured_output_dict = structured_output.dict()
    structured_output_offsets = get_structured_output_offsets(structured_output_dict,
                                                                        concatenated_text)
    for structured_output_offset in structured_output_offsets:
        ngram_start = structured_output_offset['ngram_start']
        ngram_end = structured_output_offset['ngram_end']
        ngram_confidence_percentage = get_token_probabilities_for_ngram(ngram_start, ngram_end, di_words_confidence_list)
        structured_output_offset['confidence_percentage'] = ngram_confidence_percentage
    return structured_output_offsets


def map_tokens_to_fields(response):
    structured_output = response.choices[0].message.parsed
    tokens = response.choices[0].logprobs.content
    tokens_with_offsets = get_tokens_with_offsets(tokens)
    concatenated_text = ''.join(token['token_text'] for token in tokens_with_offsets)
    structured_output_dict = structured_output.dict()
    structured_output_offsets = get_structured_output_offsets(structured_output_dict,
                                                                        concatenated_text)
    for structured_output_offset in structured_output_offsets:
        ngram_start = structured_output_offset['ngram_start']
        ngram_end = structured_output_offset['ngram_end']
        ngram_confidence_percentage = get_token_probabilities_for_ngram(ngram_start, ngram_end, tokens_with_offsets)
        structured_output_offset['confidence_percentage'] = ngram_confidence_percentage
    return structured_output_offsets


def get_tokens_with_offsets(tokens):

    tokens_with_offsets = list()
    current_position = 0

    for token_info in tokens:
        token_text = token_info.token  # The text of the token
        # token_logprob = token_info.logprob
        token_logprob = np.round(np.exp(token_info.logprob) * 100, 2)
        # Calculate the start position of the token
        start_position = current_position
        # Calculate the end position (exclusive) after adding the token's length
        end_position = start_position + len(token_text)

        # Save the token with its start and end positions
        tokens_with_offsets.append({
            'token_text': token_text,
            'token_logprob': token_logprob,
            'start': start_position,
            'end': end_position
        })

        # Update the current position for the next token
        current_position = end_position

    return tokens_with_offsets


def get_di_words_with_offsets(di_words_confidence_list):

    current_position = 0

    for di_words_confidence in di_words_confidence_list:
        word_content = di_words_confidence['word_content']  # The text of the token
        word_confidence = di_words_confidence['word_confidence']

        start_position = current_position
        end_position = start_position + len(word_content)
        di_words_confidence['token_logprob'] = word_confidence
        di_words_confidence['start'] = start_position
        di_words_confidence['end'] = end_position

        current_position = end_position

    return di_words_confidence_list



def find_ngram_offsets(text, ngram):
    start_offset = text.find(ngram)

    if start_offset != -1:
        # raise ValueError(f"N-gram '{ngram}' not found in the text.")
        end_offset = start_offset + len(ngram)
    else:
        end_offset = -1

    return start_offset, end_offset


def get_token_probabilities_for_ngram(ngram_start, ngram_end, tokens_with_offsets):

    # Step 3: Find tokens that overlap with the n-gram offsets
    result_tokens = []
    for tokens_with_offset in tokens_with_offsets:
        if tokens_with_offset['end'] > ngram_start and tokens_with_offset['start'] < ngram_end:
            result_tokens.append(tokens_with_offset)

    ngram_confidence_percentage = 1
    for token_offset in result_tokens:
        word_confidence_percentage = token_offset["token_logprob"]
        ngram_confidence_percentage = ngram_confidence_percentage * word_confidence_percentage / 100

    ngram_confidence_percentage = np.round(ngram_confidence_percentage * 100, 2)

    return str(ngram_confidence_percentage)


def get_structured_output_offsets(structured_output_dict, concatenated_text):
    fields_confidence_percentage_list = list()
    for field, value in structured_output_dict.items():
        if isinstance(value, str):
            ngram_start, ngram_end = find_ngram_offsets(concatenated_text, value)
            fields_confidence_percentage_list.append({"field":field,
                                                      "value": value,
                                                      "ngram_start": ngram_start,
                                                      "ngram_end": ngram_end})
    return fields_confidence_percentage_list