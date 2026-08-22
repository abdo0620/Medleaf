import chromadb as db
from chromadb.utils import embedding_functions
ollama_ef=embedding_functions.OllamaEmbeddingFunction(
    url= 'http://localhost:11434', 
  model= 'nomic-embed-text'
)
vector_db=db.PersistentClient("Vectordb")

def get_collec():
    return vector_db.get_or_create_collection("mrooc",embedding_function=ollama_ef)
