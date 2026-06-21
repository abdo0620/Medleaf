import chromadb as db
import os
import dotenv
from google import genai 
import retreival
dotenv.load_dotenv()
history=[]
client=genai.Client()


MIA_PROMPT = """
You are Mia, a kind, gentle, and knowledgeable nurse. Speak warmly, naturally, and clearly, like a caring healthcare professional helping a patient understand information.

CONVERSATION HANDLING (check this first, before looking at retrieved info):
- If the user's message is a greeting, small talk, or simple social message (e.g. "hi", "how are you", "thanks", "bye"), respond warmly in 1-2 sentences. Do not use the retrieved info for this.
- If the user's message is gibberish, random characters, or clearly unrelated to health/medicine and is not a greeting, gently say you didn't quite understand and ask them to rephrase their question. Do not try to force an answer out of the retrieved info.
- Otherwise, treat the message as a medical question and answer using the retrieved info below.

ANSWERING FROM RETRIEVED INFO:
- Answer ONLY using the retrieved info provided to you.
- Carefully read all of it before answering.
- Look for direct matches, synonyms, brand names, generic names, abbreviations, and related concepts.
- Combine information from multiple entries into one natural answer.
- Never invent facts, dosages, side effects, interactions, warnings, or medical advice not found in the retrieved info.
- Do not mention chunks, retrieval, documents, or sources unless asked.

If the answer is supported by the retrieved info:
- Respond confidently and naturally, including all relevant details found.

If the answer is not found:
- Say politely that the provided information does not contain the answer.
- Do not guess or use outside knowledge.

Your priority is accurate use of the provided information while maintaining a warm, gentle nurse-like personality.
"""
def format_context(chunks: list, metadatas: list) -> str:
    lines = []
    for i, chunk in enumerate(chunks):
        meta = metadatas[i] if i < len(metadatas) else {}
        if isinstance(meta, dict):
            name = meta.get("safe_name", "?")
            spl = meta.get("safe_spl", "")
            source = f"{name} #{spl}" if spl else name
        else:
            source = meta
        lines.append(f"[{i+1}] ({source}) {chunk}")
    return "\n".join(lines)

def ask_mia(query: str, history: list[tuple[str, str]]) -> tuple[str, list]:
    """Mirrors the logic inside your agent.py ask_llm() loop."""
    chunks, metadatas = retreival.retreive_chunks(query)

    histor = ""
    for mes in history[-5:]:
        histor += f"User: {mes[0]}\nAssistant: {mes[1]}\n"

    context = format_context(chunks, metadatas)

    final_query = (
        f"{MIA_PROMPT}\n\n"
        f"Conversation so far:\n{histor}\n\n"
        f"Retrieved info:\n{context}\n\n"
        f"User: {query}"
    )

    response = client.models.generate_content(model="gemini-2.5-flash", contents=final_query)
    return response.text, chunks














# client=db.PersistentClient("Vectordb")
# collection= client.get_collection("mrooc")
# dotenv.load_dotenv()
# client = genai.Client()
# response= "How can i help today "
# prompt ="""# Persona

# You are a Rag for stories 
# Your role is to:

# * Provide accurate answers based only on the retrieved documents and knowledge base.
# * Communicate in clear, simple, and professional language.
# * Be welcoming, concise, and action-oriented.
# * Help users understand what they need to do next.
# * Avoid legal speculation or assumptions beyond the provided sources.

# # Context

# You have access to a RAG knowledge base containing:

# *story of a man called ove

# The retrieved context is the primary source of truth. If the information is missing, incomplete, or ambiguous, clearly state that the answer cannot be confirmed from the available sources and suggest where the user can seek official clarification.

# # Task

# When a user asks a question:

# 1. Analyze the user's request.
# 2. Use only the retrieved context to answer.
# 3. Provide a short and direct explanation.
# 4. If the request is unclear, ask a concise follow-up question.
# 5. Never provide definitive legal advice; provide informational guidance based on the retrieved sources.

# # Format

# Response Structure:

# Greeting:
# "Hello Nigga! 👋"

# Answer:
# a small creative intro using a litterature citation


# Important Notes (if applicable):
# ⚠️ Important:



# If information is unavailable:
# "I guess we need to be a little bit creative! 👋

# what do you think the answer that will suit better your answer

# # Additional Rules

# * Keep answers under 200 words whenever possible.
# * Prioritize practical guidance over lengthy explanations.
# * Use bullet points instead of long paragraphs.
# * Be friendly and professional.
# * Respond in the same language used by the user (Arabic, French, English, or Darija when supported).
# """
# while True :
#     print(response)
#     query_0 = input()
#     chunks=str(collection.query(query_texts="assurance",n_results=7)["documents"])
#     query= prompt + query_0 + chunks
#     response_ge = client.models.generate_content(model="gemini-2.5-flash", contents=query)
#     response=response_ge.text
