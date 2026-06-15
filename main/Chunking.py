from google import genai
import os  
import dotenv
from google.genai.local_tokenizer import LocalTokenizer

dotenv.load_dotenv()

tokenizer = LocalTokenizer(model_name="gemini-2.5-flash")
def chunking(text : str, token_limit : int , jump : int ,overlap = 0 ,l=[]):
    n= len(text)
    i=jump
    if text =="":
        return l
    if len(text)<jump:
        l.append(text)
        return l
    total_tokens = 0
    while  i < n  and total_tokens < token_limit:
        
        total_tokens += tokenizer.count_tokens(text[i-jump:i]).total_tokens
        i+=jump
        print(total_tokens)
    l.append(text[:i])
    return chunking(text[i:],token_limit,overlap,jump,l)







