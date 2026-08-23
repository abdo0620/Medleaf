"""Configure the persistent Chroma database used by MedLeaf."""

import chromadb as cdb
from chromadb.utils import embedding_functions
from path import Path
PARENT_DIR=Path(__file__).parent

# Keep the embedding model and vector store configuration together so indexing
# and retrieval use the same representation space and persistent location.
ollama_ef=embedding_functions.OllamaEmbeddingFunction(
    url= 'http://localhost:11434', 
  model_name= 'nomic-embed-text'
)
vector_db=cdb.PersistentClient(PARENT_DIR / "Vectordb")

def get_collec():
  """Get or create the application's medication document collection."""
  # A stable collection name lets the application reuse the index across
  # restarts instead of rebuilding embeddings for every session.
  return vector_db.get_or_create_collection("mrooc",embedding_function=ollama_ef)
