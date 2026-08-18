"""
MedLeaf — Conversational RAG Agent for Drug Leaflet Understanding
Streamlit interface, wired to match your existing files:
    agent.py        -> Gemini call + Mia persona prompt
    retreival.py     -> retreive_chunks(query)
    Chunking.py      / initialize_db.py  (already run separately to build Vectordb)

HOW TO RUN:
    pip install streamlit google-genai python-dotenv chromadb
    streamlit run app/main.py

REQUIREMENTS:
    - Vectordb/ must already exist (run initialize_db.py once before this)
    - A .env file with your Gemini API key (GEMINI_API_KEY or GOOGLE_API_KEY)
"""
import streamlit as st
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from Rag import agent

st.set_page_config(page_title="MedLeaf", page_icon="app/assets/images/Gemini_Generated_Image_8yo9v28yo9v28yo9.png", layout="centered")


# ──────────────────────────────────────────────────────────────────────────
# Session state
# ──────────────────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []  # list of (query, answer_text)
if "display_log" not in st.session_state:
    st.session_state.display_log = []  # list of (query, answer, chunks)

# ──────────────────────────────────────────────────────────────────────────
# UI
# ──────────────────────────────────────────────────────────────────────────

st.image("app/assets/images/Gemini_Generated_Image_pjw0i6pjw0i6pjw0.png", use_container_width=True)
st.logo("app/assets/images/Gemini_Generated_Image_pjw0i6pjw0i6pjw0.png",size="large")
st.caption("Conversational RAG Agent for Drug Leaflet Understanding - talk to Mia")
st.divider()

st.chat_message("assistant",avatar="app/assets/images/female-doctor-to-explain-svgrepo-com.svg").write("Helloo, I am Mia, how can I help you today?")

for q, a, chunks in st.session_state.display_log:
    st.chat_message("user").write(q)
    with st.chat_message("assistant",avatar="app/assets/images/female-doctor-to-explain-svgrepo-com.svg"):
        st.write(a)
        with st.expander("View retrieved chunks"):
            for i, c in enumerate(chunks, 1):
                st.markdown(f"**Chunk {i}**")
                st.caption(c)

query = st.chat_input("Ask Mia about a medication...")

if query:
    st.chat_message("user").write(query)
    with st.chat_message("assistant",avatar="app/assets/images/female-doctor-to-explain-svgrepo-com.svg"):
        with st.spinner("Mia is reading the leaflets..."):
            answer, chunks = agent.ask_mia(query, st.session_state.history)
            st.write(answer)
            with st.expander("View retrieved chunks"):
                for i, c in enumerate(chunks, 1):
                    st.markdown(f"**Chunk {i}**")
                    st.caption(c)

    st.session_state.history.append((query, answer))
    st.session_state.display_log.append((query, answer, chunks))

st.divider()
st.caption("MedLeaf · (FDA API + Uploaded documents) → Chunking.py → ChromaDB → Gemini")

