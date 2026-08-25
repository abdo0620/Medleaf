"""Generate conversational answers from retrieved medication information."""

from ollama import chat
import sys 
from pathlib import Path

ROOT_DIR=Path(__file__).parent.parent

sys.path.append(str(ROOT_DIR / "retreival"))
import retreival
history=[]

# The prompt is the application's safety and grounding contract: the model is
# instructed to use retrieved leaflet text instead of relying on prior knowledge.
MIA_PROMPT = """
You are Mia, a kind, gentle, and knowledgeable nurse. Speak warmly, naturally, and clearly, like a caring healthcare professional helping a patient understand information.

CONVERSATION HANDLING (check this first, before looking at retrieved info):
- If the user's message is a greeting, small talk, or simple social message (e.g. "hi", "how are you", "thanks", "bye"), respond warmly in 1-2 sentences. Do not use the retrieved info for this.
- If the user's message is gibberish, random characters, or clearly unrelated to health/medicine and is not a greeting, gently say you didn't quite understand and ask them to rephrase their question. Do not try to force an answer out of the retrieved info.
- Otherwise, treat the message as a medical question and answer using the retrieved info below.
- Always replies using the language of the user.

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
do not any questions that do not relate to medical domaine.
"""
def format_context(chunks: list, metadatas: list) -> str:
    """Format retrieved chunks and metadata as context for the language model."""
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

def ask_mia(query: str, history: list[dict]=[]) -> tuple[str, list]:
    """Retrieve context and ask Mia to answer ``query`` using the conversation history."""
    chunks, metadatas = retreival.retreive_chunks(query)

    context = format_context(chunks, metadatas)

    final_query = (
        f"{MIA_PROMPT}\n\n"
        f"Retrieved info:\n{context}\n\n"
        f"User: {query}"
    )
    history.append({'role': 'user', 'content': final_query})

    # Bound conversational context to control latency and prevent stale turns
    # from competing with the retrieved evidence for the model's attention.
    response = chat(model='qwen2.5:3b-instruct', messages=history[-10:])
    history.append({'role':'assistant','content':response['message']['content']})
    return response['message']['content'], chunks





