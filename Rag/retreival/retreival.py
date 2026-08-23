"""Retrieve the most relevant document chunks from the Chroma collection."""

from path import Path 
import sys
ROOT_DIR = Path(__file__).parent.parent
DB_DIR=ROOT_DIR / "database" 
sys.path.append(DB_DIR)
import db 
collection=db.get_collec()

def retreive_chunks(query:str) :
    """Return up to three document chunks and their associated metadata."""

    # Keep retrieval deliberately small: a compact, relevant context reduces
    # prompt noise and limits the model's opportunity to answer from guesses.
    results=collection.query(query_texts=query,n_results=3)["documents"][0]
    metadatas=collection.query(query_texts=query,n_results=3)["metadatas"][0]
    return results,metadatas
