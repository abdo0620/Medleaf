import os
import tiktoken
# from google import genai
import dotenv 
# from chromadb.utils import embedding_functions
dotenv.load_dotenv()
import Chunking
print(Chunking.lojlo("hh"))

print(os.getenv("GEMINI_API_KEY"))
# os.chdir("files")



# print(os.getcwd())
# print(os.getcwd())

# file = open("law.txt","r")
# print(file.readline())

# reader=pypdf.PdfReader("4_ONC_Law_fr-FR.pdf")
# metadata=reader.metadata
# metadataex=reader.xmp_metadata
# print(metadata)
# print(metadataex)
# pages=reader.pages
# print(pages)
# print(pages[3])
# print(pages[158].extract_text(extraction_mode="layout")) #extrac text with roation angle 0 degree no output all angles

# ecode= tiktoken.encoding_for_model("gpt-4o")



# # print(len(pages[3].get_contents().get_data()))
# # print(reader.page_layout)
# # print(type(pages[150].extract_text()))
# # a=(ecode.encode(pages[1].extract_text(extraction_mode="layout")))
# # print(a)
# # print(len(a))
# txt=""
# for page in pages[:8]:
#     txt +=page.extract_text(extraction_mode="layout")
# ########################## chunking
# def chunking(text,token_limit,l=[],upgrate_rate=1,n=0):
#     i=0
#     if len(text)<upgrate_rate:
#         l.append(text)
#         return len(l)
#     while len(ecode.encode(text[:i]))<token_limit and i<len(txt):
#             i+=upgrate_rate
#     l.append(text[:i])
#     n+=1
#     print(n)
#     return (chunking(text[i:],token_limit,l,upgrate_rate,n))

# print(chunking(txt,1000,[],500))

# client=genai.Client()
# result=client.models.embed_content(
#     model="gemini-embedding-2",
#     contents ="hi my name is ahmed"
# )
# print(len(result.embeddings))



