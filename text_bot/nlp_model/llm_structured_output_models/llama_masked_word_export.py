from pydantic import BaseModel
from typing import Dict, List

class LlamaMaksedWordPrediction(BaseModel):
    # masked_words_prediction_list: List[str]
    masked_words_prediction_list: str