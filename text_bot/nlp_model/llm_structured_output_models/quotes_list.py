from pydantic import BaseModel
from typing import Dict

class QuotesListModel(BaseModel):
    quote1: str
    author1: str
    quote2: str
    author2: str
    quote3: str
    author3: str

