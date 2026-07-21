import chromadb as db
import os
from Rag import Chunking
import uuid
from chromadb.config import Settings
import json

vector_db=db.PersistentClient("Vectordb")
def get_collec():
    return vector_db.get_or_create_collection("mrooc")
