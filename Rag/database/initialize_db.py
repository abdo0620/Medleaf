"""Build the Chroma collection from FDA and user-uploaded documents."""

import sys
from pathlib import Path
import uuid
import json
import fitz  
CHUNK_LIMIT=210
OVERLAP=0.15
ROOT_DIR=Path(__file__).parent.parent
DIR=Path(__file__)
sys.path.append(str(ROOT_DIR))
sys.path.append(str(DIR.parent))
from Chunking import Chunking
import db

collection=db.get_collec()

def initialize_fda_drugs() -> None:
    """Read FDA text and metadata files, chunk them, and add them to Chroma."""
    # FDA records carry metadata separately from their text; preserving it on
    # every chunk keeps source attribution available during retrieval.
    doc_list=(DIR.parent / "files" / "drug_text_files").iterdir()
    j=0
    for text_path in doc_list:
        json_path = DIR.parent / "files" / "drug_json_files" / f"{text_path.stem}.json"
        data=json.loads(json_path.read_text(encoding="utf-8"))

        meta={"safe_name" : data["safe_name"],"safe_spl" : data["safe_spl"]}
        text=text_path.read_text(encoding="utf-8")
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
    doc_list = DOCS_DIR.iterdir()
    j = 0
    for file_path in doc_list:
        file_name = file_path.name

        if file_path.suffix.lower() == ".pdf":
            doc = fitz.open(str(file_path))
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

            meta = {"safe_name": file_name, "source_type": "pdf"}

            l = Chunking.rec_chunk(text, CHUNK_LIMIT, OVERLAP)
            collection.add(
                documents=l,
                ids=[str(uuid.uuid4()) for _ in range(len(l))],
                metadatas=[meta for _ in range(len(l))],
            )
            j += 1

        elif file_path.suffix.lower() == ".txt":
            text = file_path.read_text(encoding="utf-8")

            meta = {"safe_name": file_name, "source_type": "txt"}

            l = Chunking.rec_chunk(text, CHUNK_LIMIT, OVERLAP)
            collection.add(
                documents=l,
                ids=[str(uuid.uuid4()) for _ in range(len(l))],
                metadatas=[meta for _ in range(len(l))],
            )
            j += 1

          
        file_path.unlink()

