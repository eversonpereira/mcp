import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MODEL_NAME = os.getenv("MODEL_NAME", "mistral")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./chroma")
    DB_PATH = os.getenv("DB_PATH", "./mcp.db")
    CONTEXT_LIMIT = int(os.getenv("CONTEXT_LIMIT", 5))
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    SUMMARY_TRIGGER = int(os.getenv("SUMMARY_TRIGGER", 20))

settings = Settings()
