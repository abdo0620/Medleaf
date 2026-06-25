 ![MedLeaf App Interface](app/Gemini_Generated_Image_pjw0i6pjw0i6pjw0.png) 

## Project Description
MedLeaf is a research-focused application for analyzing drug leaflet content using retrieval-augmented generation (RAG).
It provides:
- a Streamlit interface for user queries and responses,
- a backend pipeline for ingestion, chunking, embedding, storage, and retrieval,
- a local vector database for semantic search,
- AI-generated answers grounded in the source documents.

The project demonstrates how AI can improve access to medical product information.

![MedLeaf App Interface](screenshots/Screenshot%202026-06-25%20204033.png)

## Key Contributions
- Streamlit user interface in `app/app.py`
- Backend architecture in `Rag/`
- Text chunking and retrieval for relevant search results
- Tokenization integration with `google-genai` and `sentencepiece`
- Docker and Docker Compose deployment
- Resolved Docker import and dependency issues

## Tools
- Python 3.12
- Streamlit
- Docker and Docker Compose
- Chroma vector database
- Google Gemini / `google-genai`
- `sentencepiece`

## Run with Docker
Run with Docker only.

### Windows
1. Install Docker Desktop.
2. Open a terminal in the project root folder.
3. Run:
   ```powershell
   docker compose up --build
   ```
4. Wait for the build to complete.
5. Open your browser and go to:
   ```text
   http://localhost:8501
   ```
5. Open your browser and go to `http://localhost:8501`.

### macOS / Linux
1. Install Docker Desktop (macOS) or Docker Engine / Docker Compose (Linux).
2. Open a terminal in the project root folder.
3. Run:
   ```bash
   docker compose up --build
   ```
4. Wait for the build to complete.
5. Open your browser and go to:
   ```text
   http://localhost:8501
   ```
5. Open your browser and go to `http://localhost:8501`.

To stop the app:
```bash
Ctrl+C

docker compose down
```

## Environment variables
1. Copy the example environment file and add the API key:

```bash
cp Rag/.env.example Rag/.env
```

2. Create file `Rag/.env` and set the Gemini API key (or Google API key):

```
GEMINI_API_KEY=your_gemini_api_key_here
# or
GOOGLE_API_KEY=your_google_api_key_here
```

3. The Docker Compose service reads `Rag/.env` (see `docker-compose.yml`).
   - Place the real API key only in `Rag/.env` and do not commit it to version control.

`Rag/.env.example` contains placeholder values to copy from.

## How the System Works
The app follows a retrieval-augmented generation workflow.

1. **Data ingestion**
   - Load raw drug leaflet text files from `files/`.
   - Normalize the text for processing.

2. **Chunking**
   - Split documents into smaller, searchable chunks.
   - Capture semantic boundaries while limiting chunk size.

3. **Embedding**
   - Convert each chunk into a numerical vector.
   - Embeddings represent semantic meaning.

4. **Vector storage**
   - Store embeddings in the `Vectordb/` vector database.
   - Retrieve relevant chunks through similarity indexing.

5. **Retrieval**
   - Convert the user's query into an embedding.
   - Find the most similar document chunks.

6. **Answer generation**
   - Send the selected chunks to the AI agent.
   - Synthesize a response grounded in retrieved content.

## Why Embedding Matters
Embeddings connect text to semantic search.
- Convert words and phrases into numeric vectors.
- Represent semantic similarity across text.
- Enable retrieval even when query wording differs.

## Project Structure
- `app/app.py` — main Streamlit application
- `Dockerfile` — Docker image definition
- `docker-compose.yml` — Docker Compose configuration
- `requirements.txt` — Python dependencies
- `Rag/` — backend logic for agent, chunking, and retrieval
- `Vectordb/` — local vector database storage
- `files/` — source data files and utilities

## Highlights
- Modern AI tooling and vector search
- Docker-based deployment
- Practical resolution of Docker dependency issues
- A user-facing interface for non-technical users


