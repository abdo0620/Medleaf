 ![MedLeaf App Interface](app/Gemini_Generated_Image_pjw0i6pjw0i6pjw0.png) 

## Project Description
MedLeaf is a research-focused application for analyzing drug leaflet content using retrieval-augmented generation (RAG). It combines a Streamlit user interface with a backend pipeline that:
- ingests pharmaceutical text data,
- creates searchable chunks,
- indexes content in a local vector database,
- and generates answers grounded in the source material.

The project demonstrates how AI can improve access to medical product information.

![MedLeaf App Interface](screenshots/Screenshot%202026-06-25%20204033.png)

## Key Contributions
- Streamlit user interface in `app/app.py`
- Backend architecture in `Rag/`
- Text chunking and retrieval for relevant search results
- Tokenization integration with `google-genai` and `sentencepiece`
- Docker and Docker Compose for consistent deployment
- Resolved Docker import and dependency issues

## Tools
- Python 3.12
- Streamlit
- Docker and Docker Compose
- Chroma vector database
- Google Gemini / `google-genai`
- `sentencepiece`

## Run with Docker
This project is designed to run with Docker only.

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

To stop the app:
```bash
Ctrl+C

docker compose down
```

## How the System Works
The app follows a retrieval-augmented generation workflow.

1. **Data ingestion**
   - Load raw drug leaflet text files from `files/`.
   - Normalize the text for processing.

2. **Chunking**
   - Split documents into smaller, searchable chunks.
   - Smaller chunks improve the relevance of search results.

3. **Embedding**
   - Convert each chunk into a numerical vector.
   - Embeddings represent semantic meaning.

4. **Vector storage**
   - Store embeddings in the `Vectordb/` vector database.
   - This enables fast similarity search.

5. **Retrieval**
   - Convert the user's query into an embedding.
   - Find the most similar document chunks.

6. **Answer generation**
   - Send the selected chunks to the AI agent.
   - Generate a response based on the retrieved information.

## Why Embedding Matters
Embeddings connect text to semantic search.
- They transform words into numeric vectors.
- Similar ideas produce similar vectors.
- This helps the system find meaning even when phrasing differs.

## Project Structure
- `app/app.py` — main Streamlit application
- `Dockerfile` — Docker image definition
- `docker-compose.yml` — Docker Compose configuration
- `requirements.txt` — Python dependencies
- `Rag/` — backend logic for agent, chunking, and retrieval
- `Vectordb/` — local vector database storage
- `files/` — source data files and utilities

## Highlights
This project demonstrates:
- modern AI tooling and vector search,
- Docker-based deployment,
- practical problem solving for Docker dependencies,
- and a usable interface for non-technical users.


