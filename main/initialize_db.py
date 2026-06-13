import chromadb as db
import pypdf 
import os
import tiktoken
import Chunking
os.chdir("files")
doc_list=os.listdir()
for i in doc_list:
    reader=pypdf.PdfReader(i)
    reader_pages=reader.pages


