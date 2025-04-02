import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(persist_directory="./chroma"))
collection = client.get_or_create_collection(name="teste")

collection.add(documents=["Oi, tudo bem?"], ids=["1"])
print(collection.query(query_texts=["tudo"], n_results=1))

