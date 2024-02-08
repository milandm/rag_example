import logging
import os
from sklearn.metrics.pairwise import paired_cosine_distances, paired_euclidean_distances, paired_manhattan_distances
from scipy.stats import pearsonr, spearmanr
import numpy as np
from typing import List

import logging
import os
from sklearn.metrics.pairwise import paired_cosine_distances, paired_euclidean_distances, paired_manhattan_distances
from scipy.stats import pearsonr, spearmanr
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer, util
from collections import OrderedDict
import tiktoken

CL100K_BASE_ENCODING_NAME = "cl100k_base"

def token_count_from_string(string: str, encoding_name: str = CL100K_BASE_ENCODING_NAME) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_mmr_cosine_sorted_docs(query_embedding, docs):
    lambda_parameter = 0.5
    similarity1 = util.pytorch_cos_sim
    similarity2 = util.pytorch_cos_sim
    return mmr_sorted(query_embedding, docs, lambda_parameter, similarity1, similarity2)

def mmr_sorted(query_embedding, docs_embeddings, lambda_parameter, similarity1, similarity2):
    """Sort a list of docs by Maximal marginal relevance

	Performs maximal marginal relevance sorting on a set of
	documents as described by Carbonell and Goldstein (1998)
	in their paper "The Use of MMR, Diversity-Based Reranking
	for Reordering Documents and Producing Summaries"

    :param docs: a set of documents to be ranked
				  by maximal marginal relevance
    :param q: query to which the documents are results
    :param lambda_: lambda parameter, a float between 0 and 1
    :param similarity1: sim_1 function. takes a doc and the query
						as an argument and computes their similarity
    :param similarity2: sim_2 function. takes two docs as arguments
						and computes their similarity score
    :return: a (document, mmr score) ordered dictionary of the docs
			given in the first argument, ordered my MMR
    """
    selected = OrderedDict()
    docs_embeddings = set(docs_embeddings)
    while set(selected) != docs_embeddings:
        remaining = docs_embeddings - set(selected)
        mmr_score = lambda x: lambda_parameter * similarity1(x_embedding, query_embedding) - (1 - lambda_parameter) * max(
            [similarity2(x_embedding, y_embedding) for y in set(selected) - {x}] or [0])
        next_selected = max(remaining, key=mmr_score)
        selected[next_selected] = len(selected)
    return selected


def get_distance_scores(embeddings1, embeddings2):
    cosine_scores = 1 - (paired_cosine_distances([embeddings1], [embeddings2]))
    manhattan_distances = paired_manhattan_distances([embeddings1], [embeddings2])
    euclidean_distances = paired_euclidean_distances([embeddings1], [embeddings2])
    dot_products = [np.dot(emb1, emb2) for emb1, emb2 in zip([embeddings1], [embeddings2])]
    cos_sim_score_transformer = util.pytorch_cos_sim(embeddings1, embeddings2)

    distance_scores = {"cosine_scores": cosine_scores[0],
                       "manhattan_distances": manhattan_distances[0],
                       "euclidean_distances": euclidean_distances[0],
                       "dot_products": dot_products[0],
                       "cos_sim_score_transformer": cos_sim_score_transformer[0]}

    return distance_scores


def check_distance_scores_out(distance_scores):
    COSINE_SCORES_MAX_OUT = 0.6
    COSINE_SCORES_MIN_IN = 0.6
    DOT_PRODUCTS_MIN_IN = 0.7

    MANHATTAN_DISTANCES_MAX_IN = 15
    EUCLIDEAN_DISTANCES_MAX_IN = 0.75

    return distance_scores["cosine_scores"] < COSINE_SCORES_MAX_OUT \
        and distance_scores["dot_products"] < DOT_PRODUCTS_MIN_IN \
        and distance_scores["manhattan_distances"] > MANHATTAN_DISTANCES_MAX_IN \
        and distance_scores["euclidean_distances"] > EUCLIDEAN_DISTANCES_MAX_IN


@staticmethod
def is_close(a, b, threshold):
    return abs(a - b) <= threshold