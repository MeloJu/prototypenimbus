# Application configuration and constants.

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_PATH = BASE_DIR / "knowledge_base.json"
CHROMA_DB_PATH = BASE_DIR / "chroma_db"

# Ollama Configuration
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "30"))

# ChromaDB Collections
TRACKS_COLLECTION = "tracks"
MARKETING_COLLECTION = "marketing"

# Agent Configuration
MAX_RECENT_GENRES = 5
GENRE_AVOIDANCE_WINDOW = 3
BILLING_SUCCESS_RATE = 0.95
SUBSCRIPTION_PRICE = 1.0

# Time-based mood mapping
MOOD_BY_TIME = {
    "morning": ["uplifting", "energetic", "happy"],
    "afternoon": ["focused", "calm", "productive"],
    "evening": ["relaxing", "dreamy", "chill"]
}

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"



