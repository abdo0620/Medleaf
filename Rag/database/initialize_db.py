"""Build the Chroma collection from FDA and user-uploaded documents."""

import os
import sys
from path import Path
import uuid
import json
import fitz  
CHUNK_LIMIT=210
OVERLAP=0.15
ROOT_DIR=Path(__file__).parent.parent
DIR=Path(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(DIR.parent)
from Chunking import Chunking
import db

collection=db.get_collec()

def initialize_fda_drugs() -> None:
    """Read FDA text and metadata files, chunk them, and add them to Chroma."""
    # FDA records carry metadata separately from their text; preserving it on
    # every chunk keeps source attribution available during retrieval.
    doc_list=os.listdir(DIR.parent / "files" / "drug_text_files")
    j=0
    for i in doc_list:
        reader=open(DIR.parent / "files" / "drug_text_files" / i,"r",encoding="utf-8")
        jsoni =open(DIR.parent / "files" / "drug_json_files" / (i[:len(i)-3]+"json"),"r")
        data=json.load(jsoni)

        meta={"safe_name" : data["safe_name"],"safe_spl" : data["safe_spl"]}
        text=reader.read()
        l=[]
        l += Chunking.rec_chunk(text,CHUNK_LIMIT,OVERLAP)
        collection.add( documents = l , ids=[str(uuid.uuid4()) for _ in range(len(l))],metadatas=[meta for _ in range(len(l))])
        j+=1
        print(j)



DOCS_DIR = DIR.parent / "files" / "documents_injected"

def add_vector_db() -> None:
    """Index uploaded PDF and TXT documents, then remove their source files."""

    # Uploaded files are treated as a one-time ingestion queue. Removing each
    # source after indexing prevents accidental duplicate embeddings on reruns.
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

            l = Chunking.rec_chunk(text, CHUNK_LIMIT, OVERLAP)
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

            l = Chunking.rec_chunk(text, CHUNK_LIMIT, OVERLAP)
            collection.add(
                documents=l,
                ids=[str(uuid.uuid4()) for _ in range(len(l))],
                metadatas=[meta for _ in range(len(l))],
            )
            j += 1

          
        os.remove(file_path)

