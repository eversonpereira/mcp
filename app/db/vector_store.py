import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings

client = None
collection = None

def initialize_vector_store():
    global client, collection
    client = chromadb.Client(ChromaSettings(persist_directory=settings.VECTOR_DB_PATH))
    collection = client.get_or_create_collection(name="mcp_memory")

def add_to_vector_store(user_id: str, session_id: str, text: str):
    global collection
    doc_id = f"{user_id}_{session_id}_{hash(text)}"
    collection.add(documents=[text], ids=[doc_id], metadatas={"user_id": user_id, "session_id": session_id})

def query_similar_context(user_id: str, session_id: str, query: str, top_k: int = 3):
    global collection
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={
            "$and": [
                {"user_id": user_id},
                {"session_id": session_id}
            ]
        }
    )
    return results.get("documents", [[]])[0]
