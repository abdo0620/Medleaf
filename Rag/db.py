import chromadb as db
import os

vector_db=db.PersistentClient("Vectordb")

def get_collec():
    return vector_db.get_or_create_collection("mrooc")
