"""Streamlit page describing the MedLeaf project and its author."""

import streamlit as st
import base64
from pathlib import Path
DIR=Path(__file__)
def icon_src(path: str) -> str:
    """Turn a local PNG into a data URI so it can be used in an <img> tag
    inside st.markdown HTML (Streamlit doesn't serve arbitrary local files)."""
    p = Path(path)
    if not p.exists():
        return ""
    data = base64.b64encode(p.read_bytes()).decode()
    return f"data:image/png;base64,{data}"

st.set_page_config(page_title="About Me - MedLeaf", page_icon="app/assets/images/female-doctor-to-explain-svgrepo-com.svg", layout="centered")
st.logo(str(DIR.parent.parent / Path("assets/images/female-doctor-to-explain-svgrepo-com.svg")),size="large")

# ---------- styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap');

.stApp {
    background: #fafafa;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 { font-family: 'Fraunces', serif !important; }

.card {
    background: #ffffff;
    border: 1px solid #e5e5e5;
    border-radius: 14px;
    padding: 26px 30px;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
.card p, .card li { color: #3a3a3a; font-size: 15.5px; line-height: 1.65; }
.card h3 { color: #1a1a1a; margin-bottom: 10px; font-weight: 600; font-size: 20px; }

.hero-title { color: #1a1a1a; font-size: 38px; font-weight: 600; margin-bottom: 4px; }
.hero-sub { color: #8a8a8a; font-size: 14px; letter-spacing: .04em; text-transform: uppercase; margin-bottom: 26px; }

.pill {
    display: inline-block;
    background: #f0f0f0;
    border: 1px solid #dcdcdc;
    color: #4a4a4a;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 12.5px;
    margin: 4px 6px 4px 0;
    font-family: 'Inter', sans-serif;
}

.quip { color: #8a8a8a; font-style: italic; font-size: 14px; }

.contact-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
}
.contact-link {
    flex: 1 1 160px;
    display: flex;
    align-items: center;
    gap: 12px;
    background: #fafafa;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    padding: 14px 16px;
    text-decoration: none !important;
    transition: border-color .15s ease, background .15s ease;
}
.contact-link:hover { border-color: #c98a2c; background: #ffffff; }
.contact-link .icon { font-size: 20px; }
.contact-link .icon img { width: 22px; height: 22px; object-fit: contain; display: block; }
.contact-link .label { font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: #9a9a9a; }
.contact-link .value { font-size: 14px; color: #1a1a1a; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ---------- hero ----------
st.markdown("""
<div class="hero-title">About the Guy Behind MedLeaf</div>
<div class="hero-sub">Data Engineering & AI · Brest, France</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<p>I'm <b>Abdel Moujib Begdouri Terraf</b>, originally from <b>Tangier, Morocco</b>,
currently studying data engineering and AI at <b>IMT Atlantique</b> in Brest, France.
I spend most of my time convincing messy data to behave - with mixed but improving results.</p>
</div>
""", unsafe_allow_html=True)

# ---------- why medleaf ----------
st.markdown("""
<div class="card">
<h3>🌿 Why I built MedLeaf</h3>
<p>Medication leaflets are dense, inconsistent, and written like nobody expects
you to actually read them. <b>MedLeaf</b> is a local retrieval-augmented generation (RAG)
system built with <b>Ollama</b> and <b>ChromaDB</b> that indexes drug leaflets and answers 
questions in plain language, grounded in the real source text - no API calls, no external dependencies, 
completely open-source and running on your machine.</p>
<p class="quip">Basically: the leaflet does the reading through Mia, so you don't have to
unfold a piece of paper the size of a bedsheet.</p>
</div>
""", unsafe_allow_html=True)

# ---------- background ----------
st.markdown("""
<div class="card">
<h3>🧠 Background</h3>
<p>My work centers on building reliable, open-source AI systems that you can run locally -
vector database design, retrieval pipelines, semantic search, and integrating LLMs 
(Ollama, transformers) without relying on external APIs. MedLeaf applies that philosophy 
to a domain where accuracy and transparency matter: grounding medical information in 
actual source documents instead of letting models confidently hallucinate.</p>
</div>
""", unsafe_allow_html=True)

# ---------- skills ----------
st.markdown("""
<div class="card">
<h3>⚙️ Skills</h3>
<p><b>Data engineering:</b> Python (Pandas, NumPy), ETL pipelines, API integration</p>
<p><b>ML / AI:</b> RAG systems, vector databases, local LLM deployment (Ollama), 
semantic search, conversational agents</p>
<p><b>Foundations:</b> algorithms, statistics, applied ML, information retrieval</p>
<div>
<span class="pill">Python</span>
<span class="pill">RAG</span>
<span class="pill">Ollama</span>
<span class="pill">ChromaDB</span>
<span class="pill">Vector DBs</span>
<span class="pill">Streamlit</span>
<span class="pill">LLMs</span>
</div>
</div>
""", unsafe_allow_html=True)

# ---------- contact ----------
# Point these at your own icon PNGs, e.g. "icons/email.png"
icon_email = icon_src(str(DIR.parent.parent / Path("assets/logos/Gmail_Logo_512px.webp")))
icon_github = icon_src(str(DIR.parent.parent / Path("assets/logos/github.png")))
icon_linkedin = icon_src(str(DIR.parent.parent / Path("assets/logos/LinkedIn_logo_initials.png")))
icon_kaggle = icon_src(str(DIR.parent.parent / Path("assets/logos/kaggle_logo_icon_168473.png")))

st.markdown(f"""
<div class="card">
<h3> Get in touch :)</h3>
<div class="contact-grid">
  <a class="contact-link" href="mailto:abdel-moujib.begdouri-terraf@imt-atlantique.net">
    <span class="icon"><img src="{icon_email}"></span>
    <span><span class="label">Email</span><br><span class="value">Say hello</span></span>
  </a>
  <a class="contact-link" href="https://github.com/abdo0620" target="_blank">
    <span class="icon"><img src="{icon_github}"></span>
    <span><span class="label">GitHub</span><br><span class="value">abdo0620</span></span>
  </a>
  <a class="contact-link" href="https://www.linkedin.com/in/abdel-moujib-begdouri-terraf-165748288" target="_blank">
    <span class="icon"><img src="{icon_linkedin}"></span>
    <span><span class="label">LinkedIn</span><br><span class="value">Connect</span></span>
  </a>
  <a class="contact-link" href="https://www.kaggle.com/abdelmoujib" target="_blank">
    <span class="icon"><img src="{icon_kaggle}"></span>
    <span><span class="label">Kaggle</span><br><span class="value">Profile</span></span>
  </a>
</div>
</div>
""", unsafe_allow_html=True)

st.info("📬 Open to Data / AI internships.")