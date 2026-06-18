import chromadb as db
import os
import Chunking
import uuid
from chromadb.config import Settings
doc_list=os.listdir("files/drug_text_files")
vector_db=db.PersistentClient("Vectordb",settings=Settings(allow_reset=True))
vector_db.reset()
collection=vector_db.get_or_create_collection("mrooc")
for i in doc_list:
    reader=open("files/drug_text_files/" + i,"r",encoding="utf-8")
    text=reader.read()
    l=[]
    l += Chunking.rec_chunk(text,1000,0.15)
    print(i)
    collection.add( documents = l , ids=[str(uuid.uuid4()) for _ in range(len(l))])

print("Your documents are loaded")

