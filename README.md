# MedLeaf

MedLeaf is a Streamlit application for exploring medication leaflets with a retrieval-augmented generation (RAG) assistant. Users can ask Mia questions about indexed drug information, inspect the retrieved text chunks, and upload PDF or TXT leaflets to add to the local knowledge base.

The assistant runs locally with Ollama and the `qwen2.5:3b-instruct` model. Answers are generated from text retrieved from a persistent Chroma database rather than from a hosted Gemini API.

![MedLeaf interface](Rag/app/assets/images/Gemini_Generated_Image_pjw0i6pjw0i6pjw0.png)

> MedLeaf is an educational document-search tool, not a substitute for a doctor, pharmacist, or official medication leaflet. Always verify medical decisions with a qualified professional.

## App showcase
The application has three Streamlit pages:

- **Talk To Mia** — ask questions about the indexed medication documents.
- **Upload Your Documents** — add PDF or TXT files to the ingestion queue and index them.
- **About me** — project and author information.

### Main interface
![Main app interface](screenshots/Screenshot%202026-07-22%20121857.png)



### Document upload flow
![Upload documents](screenshots/Screenshot%202026-07-22%20122503.png)


## How it works
1. FDA label data is downloaded into `Rag/database/files/` by `Rag/database/files/add.py`.
2. `Rag/database/inject_fda_db.py` chunks the FDA text and stores embeddings in Chroma.
3. A user asks Mia a question in the Streamlit chat.
4. The retriever returns the three most relevant chunks from the `mrooc` collection.
5. Ollama generates an answer using those chunks and the conversation history.
6. Uploaded PDF and TXT files are chunked, embedded, and removed from the temporary ingestion queue after indexing.

## Technologies
- Python 3.12
- Streamlit 1.58
- ChromaDB 1.5.9 for persistent vector storage
- Ollama with `qwen2.5:3b-instruct` for local answer generation
- PyMuPDF for PDF text extraction
- `tiktoken` for token counting during chunking
- Docker and Docker Compose configuration

## Prerequisites
- Docker Desktop on Windows and macOS, or Docker Engine with Compose on Linux
- Ollama installed and running
- The Ollama model `qwen2.5:3b-instruct`

## Run with Docker
From the project root, build and start the application:

```bash
docker compose up --build
```

The application is then available at [http://localhost:8501](http://localhost:8501). Ollama must be running where the application can reach it, and the model must be downloaded before asking questions:

```bash
ollama serve
ollama pull qwen2.5:3b-instruct
```

To stop the application, press `Ctrl+C`. To stop and remove the container, run:

```bash
docker compose down
```

The Compose configuration persists the Chroma database and document files through mounted volumes, so indexed data remains available after the container is restarted.

## Run locally
From the project root, create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .env
.env/Scripts/activate       # Windows PowerShell
source .env/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Launch the application:

```bash
streamlit run Rag/app/main.py
```

## Populate the FDA database
The repository includes FDA label data under `Rag/database/files/`. To download a fresh set of human prescription labels and index it:

```bash
python Rag/database/files/add.py
python Rag/database/inject_fda_db.py
```

The indexed data is persisted in `Rag/database/Vectordb/`. Run the injection step again only when you want to add newly downloaded data.

## Upload documents
Use the **Upload Your Documents** page to upload PDF or TXT leaflets. The page sends files to the ingestion queue, chunks and embeds them, adds them to Chroma, and removes the queued source files after successful processing.

## Project structure
```text
Rag/
├── agent/                  # Mia prompt and Ollama integration
├── app/
│   ├── main.py             # Streamlit navigation entry point
│   ├── assets/             # Logos and assistant avatar
│   └── pages/              # Chat, upload, and About pages
├── Chunking/               # Recursive token-aware text chunking
├── database/
│   ├── db.py               # Persistent Chroma client and collection
│   ├── initialize_db.py    # FDA and uploaded-document indexing
│   ├── inject_fda_db.py    # FDA indexing script
│   └── files/              # FDA data and document ingestion folders
└── retreival/              # Similarity search over Chroma
eval/                       # Evaluation data and test script
requirements.txt            # Python dependencies
```

## Configuration
No Gemini or Google API key is required. Ollama must be available at its default local endpoint, and the model name used by the application is configured directly in `Rag/agent/agent.py`:

```text
qwen2.5:3b-instruct
```
