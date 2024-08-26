from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Iterable, Type, Union, Callable, Optional, Generator, Any
from numpy import ndarray
from pydantic import BaseModel


class NlpModel(ABC):

    # VECTOR_PARAMS_SIZE = 384
    VECTOR_PARAMS_SIZE = 1536
    # VECTOR_PARAMS_SIZE = 3072

    @abstractmethod
    def get_embeddings(self, sentences: Union[str, List[str]]) -> ndarray:
        pass

    @abstractmethod
    def get_embedding(self, text:str):
        pass

    @abstractmethod
    def send_prompt( self, system_msg:str, user_prompt:str ):
        pass


    @abstractmethod
    def send_prompt_structured_output(self, system_msg: str,
                                      user_prompt: str,
                                      structured_output_model: BaseModel):
        pass