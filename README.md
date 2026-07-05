![MedLeaf App Interface](app/Gemini_Generated_Image_pjw0i6pjw0i6pjw0.png)

## Project Description
MedLeaf is a research-oriented application for the analysis of drug leaflet content through a Retrieval-Augmented Generation (RAG) pipeline. The system combines a Streamlit-based user interface with a backend pipeline responsible for ingesting pharmaceutical text data, constructing searchable text segments, indexing content in a local vector database, and generating answers grounded in the source material. The project illustrates the applicability of contemporary retrieval-augmented methods to improving access to medical product information.

![MedLeaf App Interface](screenshots/Screenshot%202026-06-25%20204033.png)

## I. General Architecture

The system is structured around a set of functional components operating in sequence to render pharmaceutical information searchable and interpretable:

- **Data ingestion**: loading of raw drug leaflet text files from `files/`, followed by text normalization for downstream processing.
- **Chunking**: module responsible for the segmentation of documents into smaller, searchable units. Reduced chunk granularity is intended to improve the relevance of subsequent search operations.
- **Embedding and vector storage**: component responsible for the conversion of each chunk into a numerical vector representing its semantic content, and for the storage of these vectors in a local **Chroma** vector database (`Vectordb/`) to enable efficient similarity search.
- **Retrieval and answer generation**: the user query is converted into an embedding, the most semantically similar chunks are retrieved, and the resulting context is submitted to the AI agent (based on **Google Gemini / google-genai**) for grounded response generation.
- **Application layer**: a **Streamlit** interface (`app/app.py`) through which users submit queries and consult generated responses.

The project is designed to be executed exclusively within a Docker environment, in order to ensure reproducibility, service isolation, and consistency of deployment across systems.

## II. Execution Procedure

### II.1. Requirements

The project requires a Docker-based environment:

- **Docker Desktop** (Windows / macOS)
- **Docker Engine / Docker Compose** (Linux)
- A **Google Gemini API key**

### II.2. Environment Configuration

Before building the container, copy the example environment file and add your API key:

**Windows / macOS / Linux**

1. Navigate to the `Rag/` folder.
2. Copy `.env.example` to `.env`:
```
   cp .env.example .env
```
   (On Windows, you can also duplicate the file and rename it manually.)
3. Open `.env` and add your Google Gemini API key:
```
   GEMINI_API_KEY=your_api_key_here
```

### II.3. Container Initialization

**Windows**

1. Install Docker Desktop.
2. Open a terminal in the project root directory.
3. Execute:
```
   docker compose up --build
```
4. Await completion of the build process.
5. Access the interface at: `http://localhost:8501`

**macOS / Linux**

1. Install Docker Desktop (macOS) or Docker Engine / Docker Compose (Linux).
2. Open a terminal in the project root directory.
3. Execute:
```
   docker compose up --build
```
4. Await completion of the build process.
5. Access the interface at: `http://localhost:8501`

**Note:** The `--build` flag ensures that the image is rebuilt with the dependencies specified in `requirements.txt`, including `google-genai` and `sentencepiece`. Upon completion of the build, all services are operational and the interface is available for use.

### II.4. Termination

To terminate the application:
```
Ctrl+C
```
followed by:
```
docker compose down
```

## III. System Workflow

The application implements a retrieval-augmented generation workflow composed of the following stages:

1. **Data ingestion** — Raw drug leaflet text files are loaded from `files/` and normalized for processing.
2. **Chunking** — Documents are segmented into smaller, searchable units; reduced chunk size is associated with improved retrieval relevance.
3. **Embedding** — Each chunk is converted into a numerical vector encoding its semantic content.
4. **Vector storage** — Embeddings are stored in the `Vectordb/` database (Chroma) to enable efficient similarity search.
5. **Retrieval** — The user query is embedded and compared against stored vectors to identify the most similar document chunks.
6. **Answer generation** — Retrieved chunks are submitted to the AI agent, which generates a response grounded in the retrieved content.

The quality of each stage is dependent on the preceding one; retrieval accuracy, in particular, is directly conditioned by the quality of the chunking and embedding stages.

## IV. Role of Embedding in Semantic Search

Embeddings constitute the mechanism through which textual content is rendered searchable at the semantic level:

- They map textual units to numerical vector representations.
- Semantically related content is mapped to proximate vectors.
- This property enables the system to identify relevant content irrespective of variation in phrasing.

## V. Project Structure

- `app/app.py` — main Streamlit application
- `Dockerfile` — Docker image definition
- `docker-compose.yml` — Docker Compose configuration
- `requirements.txt` — Python dependencies
- `Rag/` — backend logic for the agent, chunking, and retrieval components
- `Vectordb/` — local vector database storage
- `files/` — source data files and associated utilities

## VI. Tools and Dependencies

- Python 3.12
- Streamlit
- Docker and Docker Compose
- Chroma vector database
- Google Gemini / google-genai
- sentencepiece
