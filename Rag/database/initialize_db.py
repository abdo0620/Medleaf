import os
import Rag.agent.Chunking.Chunking as Chunking
import uuid
import json
from . import db
import fitz  

collection=db.get_collec()

def initialize_fda_drugs() -> None:
    doc_list=os.listdir("files/drug_text_files")
    j=0
    for i in doc_list:
        reader=open("files/drug_text_files/" + i,"r",encoding="utf-8")
        jsoni =open("files/drug_json_files/"+i[:len(i)-3]+"json","r")
        data=json.load(jsoni)

        meta={"safe_name" : data["safe_name"],"safe_spl" : data["safe_spl"]}
        text=reader.read()
        l=[]
        l += Chunking.rec_chunk(text,600,0.15)
        collection.add( documents = l , ids=[str(uuid.uuid4()) for _ in range(len(l))],metadatas=[meta for _ in range(len(l))])
        j+=1
        print(j)



DOCS_DIR = "files/documents_injected"

def add_vector_db() -> None:

    doc_list = os.listdir(DOCS_DIR)
    j = 0
    for i in doc_list:
        file_path = os.path.join(DOCS_DIR, i)

        if i.lower().endswith(".pdf"):
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

            meta = {"safe_name": i, "source_type": "pdf"}

            l = Chunking.rec_chunk(text, 600, 0.15)
            collection.add(
                documents=l,
                ids=[str(uuid.uuid4()) for _ in range(len(l))],
                metadatas=[meta for _ in range(len(l))],
            )
            j += 1

        elif i.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as reader:
                text = reader.read()

            meta = {"safe_name": i, "source_type": "txt"}

            l = Chunking.rec_chunk(text, 1000, 0.15)
            collection.add(
                documents=l,
                ids=[str(uuid.uuid4()) for _ in range(len(l))],
                metadatas=[meta for _ in range(len(l))],
            )
            j += 1

          
        os.remove(file_path)

