import os
from Rag import Chunking
import fitz  
from google.genai.local_tokenizer import LocalTokenizer


DOCS_DIR = "files/documents_injected"


tokenizer = LocalTokenizer(model_name="gemini-2.5-flash")

def piwpiw() -> None:

    doc_list = os.listdir(DOCS_DIR)
    for i in doc_list:
        file_path = os.path.join(DOCS_DIR, i)

        if i.lower().endswith(".pdf"):
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

           

            l = zip(Chunking.rec_chunk(text, 800, 0.15),[tokenizer.count_tokens(texto).total_tokens for texto in Chunking.rec_chunk(text, 800, 0.15) ])
            return l

        elif i.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as reader:
                text = reader.read()

         
            l = zip(Chunking.rec_chunk(text, 800, 0.15),[tokenizer.count_tokens(text).total_tokens for text in Chunking.rec_chunk(text, 800, 0.15) ])
            return (l)

          
