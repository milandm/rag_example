from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Iterable, Type, Union, Callable, Optional, Generator, Any
from numpy import ndarray

class MmlModel(ABC):

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
    def generate_image(self, image_description_prompt:str):
        pass