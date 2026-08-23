
"""Split documents into token-limited chunks with optional overlap."""

from path import Path 
import sys
PARENT_DIR  = Path(__file__).parent 
sys.path.append(PARENT_DIR)
from tokenizer import count_tokens_ollama
sep = ["\n\n","\n",".",","]

def closest_space(text:str,overlap:float) ->  str:
    """Extract the trailing words used to overlap adjacent chunks."""
    assert 0 <= overlap and overlap <= 1,"overlap value must be bettween 0 and 1"
    n=text.split(" ")
    m = int(overlap*len(n))
    new_text=""
    for i in range(len(n)-m,len(n)):
        new_text+= n[i] + " "
    return new_text.strip()

def overlaping(chunks:list[str],overlap : float) -> list[str]:
    """Add an overlap from each preceding chunk to the next chunk."""
    assert 0 <= overlap and overlap <= 1,"overlap value must be bettween 0 and 1"
    if chunks==[]:
        return []
    new_chunks=[chunks[0]]
    for i in range(1,len(chunks)):
        new_chunks.append(closest_space(chunks[i-1],overlap)+" | " +chunks[i])
    return new_chunks

def chunking(text: str, token_limit: int, sepa=sep) -> list[str]:
    """Recursively split ``text`` so each returned chunk fits the token limit."""
    # Start with semantic boundaries and progressively fall back to smaller
    # separators; this preserves leaflet structure better than fixed slicing.
    text = text.strip()
    if text == "":
        return []
    if count_tokens_ollama(text) < token_limit:
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
        if count_tokens_ollama(p) >= token_limit:
            processed.extend(chunking(p, token_limit, sepa=next_sepa))
        else:
            processed.append(p)

    # Recombine small pieces after recursive splitting to avoid unnecessarily
    # short retrieval units and improve the context available to the LLM.
    merged = []
    current = ""
    for piece in processed:
        candidate = piece if current == "" else current + separator + piece
        if count_tokens_ollama(candidate)< token_limit:
            current = candidate
        else:
            if current:
                merged.append(current)
            current = piece
    if current:
        merged.append(current)

    return merged

def rec_chunk(text:str,token_limit:int,overlap:float,sepa=sep) -> list[str]:
    """Chunk text and add the requested fractional overlap between chunks."""
    return overlaping(chunking(text,token_limit,sepa),overlap )



