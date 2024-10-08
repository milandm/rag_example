import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths
ROOT = Path(__file__).parent
DATA = ROOT / "data"
MAX_SENTENCE_LENGTH = 100

# Qdrant
QDRANT_PORT = os.getenv("QDRANT_HOST")
QDRANT_HOST = os.getenv("QDRANT_PORT")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "meditations-collection_4"

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
