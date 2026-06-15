import chromadb as db
import pypdf 
import os
import tiktoken
import Chunking
import uuid
from chromadb.config import Settings
doc_list=os.listdir("files/")
vector_db=db.PersistentClient("Vectordb",settings=Settings(allow_reset=True))
vector_db.reset()
collection=vector_db.get_or_create_collection("mrooc")
for i in doc_list:
    reader=pypdf.PdfReader("files/" + i)
    reader_pages=reader.pages
    j=0
    for page in reader_pages:
        l=Chunking.chunking(page.extract_text(extraction_mode="layout"),1000,300)
        collection.add( documents =l , ids=[str(uuid.uuid4()) for _ in range(len(l))] )

print("Your documents are loaded")

