import dotenv
from google.genai.local_tokenizer import LocalTokenizer

dotenv.load_dotenv()
sep = ["\n\n","\n",".",","]
tokenizer = LocalTokenizer(model_name="gemini-2.5-flash")

def closest_space(text:str,overlap:float):
    assert 0 <= overlap and overlap <= 1,"overlap value must be bettween 0 and 1"
    n=text.split(" ")
    m = int(overlap*len(n))
    new_text=""
    for i in range(len(n)-m,len(n)):
        new_text+= n[i] + " "
    return new_text.strip()
print(closest_space("fjf fjf jf f fjf f f fjf f  ggggggggggg",3))

def overlaping(chunks,overlap ):
    assert 0 <= overlap and overlap <= 1,"overlap value must be bettween 0 and 1"
    if chunks==[]:
        return []
    new_chunks=[chunks[0]]
    for i in range(1,len(chunks)):
        new_chunks.append(closest_space(chunks[i-1],overlap)+" | " +chunks[i])
    return new_chunks

        




def chunking(text : str, token_limit : int ,sepa = sep):
    text=text.strip()
    if text=="":
        return []
    elif tokenizer.count_tokens(text).total_tokens < token_limit:
        return [text]
    elif sepa==[]:
        return [text]

    parts=text.split(sepa[0])
    l=[]
    next_sepa = sepa[1:] 
    for i in range(len(parts)):        
        l+=chunking( parts[i] ,token_limit,sepa=next_sepa)
    
    return (l)



def rec_chunk(text,token_limit,overlap,sepa=sep):
    return overlaping(chunking(text,token_limit,sepa),overlap )



