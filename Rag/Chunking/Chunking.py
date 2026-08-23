import dotenv
import requests
from path import Path 
import sys
PARENT_DIR  = Path(__file__).parent 
sys.path.append(PARENT_DIR)
from tokenizer import count_tokens_ollama
sep = ["\n\n","\n",".",","]

def closest_space(text:str,overlap:float) ->  str:
    assert 0 <= overlap and overlap <= 1,"overlap value must be bettween 0 and 1"
    n=text.split(" ")
    m = int(overlap*len(n))
    new_text=""
    for i in range(len(n)-m,len(n)):
        new_text+= n[i] + " "
    return new_text.strip()

def overlaping(chunks:list[str],overlap : float) -> list[str]:
    assert 0 <= overlap and overlap <= 1,"overlap value must be bettween 0 and 1"
    if chunks==[]:
        return []
    new_chunks=[chunks[0]]
    for i in range(1,len(chunks)):
        new_chunks.append(closest_space(chunks[i-1],overlap)+" | " +chunks[i])
    return new_chunks

def chunking(text: str, token_limit: int, sepa=sep) -> list[str]:
    text = text.strip()
    if text == "":
        return []
    if count_tokens_ollama(text).total_tokens < token_limit:
        return [text]
    if sepa == []:
        return [text] 

    separator = sepa[0]
    next_sepa = sepa[1:]
    parts = text.split(separator)

    processed = []
    for p in parts:
        p = p.strip()
        if p == "":
            continue
        if count_tokens_ollama(p).total_tokens >= token_limit:
            processed.extend(chunking(p, token_limit, sepa=next_sepa))
        else:
            processed.append(p)

    merged = []
    current = ""
    for piece in processed:
        candidate = piece if current == "" else current + separator + piece
        if count_tokens_ollama(candidate).total_tokens < token_limit:
            current = candidate
        else:
            if current:
                merged.append(current)
            current = piece
    if current:
        merged.append(current)

    return merged

def rec_chunk(text:str,token_limit:int,overlap:float,sepa=sep) -> list[str]:
    return overlaping(chunking(text,token_limit,sepa),overlap )



