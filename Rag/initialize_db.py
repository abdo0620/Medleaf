import chromadb as db
import os
from . import Chunking
import uuid
from chromadb.config import Settings
import json
doc_list=os.listdir("files/drug_text_files")
vector_db=db.PersistentClient("Vectordb",settings=Settings(allow_reset=True))
vector_db.reset()
print()
collection=vector_db.get_or_create_collection("mrooc")
j=0
for i in doc_list:
    reader=open("files/drug_text_files/" + i,"r",encoding="utf-8")
    jsoni =open("files/drug_json_files/"+i[:len(i)-3]+"json","r")
    data=json.load(jsoni)

    meta={"safe_name" : data["safe_name"],"safe_spl" : data["safe_spl"]}
    text=reader.read()
    l=[]
    l += Chunking.rec_chunk(text,1000,0.15)
    collection.add( documents = l , ids=[str(uuid.uuid4()) for _ in range(len(l))],metadatas=[meta for _ in range(len(l))])
    j+=1
    print(j)

print("Your documents are loaded")

