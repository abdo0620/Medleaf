import chromadb as cdb
from chromadb.utils import embedding_functions
from path import Path
PARENT_DIR=Path(__file__).parent
ollama_ef=embedding_functions.OllamaEmbeddingFunction(
    url= 'http://localhost:11434', 
  model_name= 'nomic-embed-text'
)
vector_db=cdb.PersistentClient(PARENT_DIR / "Vectordb")

def get_collec():
    return vector_db.get_or_create_collection("mrooc",embedding_function=ollama_ef)
