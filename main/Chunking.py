from google import genai
import os  
import dotenv
dotenv.load_dotenv()
client = genai.Client()
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
        
        total_tokens += client.models.count_tokens(model="gemini-3.5-flash",contents=text[i-jump:i]).total_tokens
        i+=jump
    l.append(text[:i])
    return chunking(text[i:],token_limit,overlap,jump,l)
text=open("files/law.txt","r")
print(len(chunking(text.read(3300),1000,100)))






