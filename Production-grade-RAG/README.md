# RAG Engine for Document Question Answering

## Overview

This project is a Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents and ask questions based on their contents. The system retrieves relevant information from uploaded documents and uses a Large Language Model (LLM) to generate context-aware answers.

The project demonstrates document processing, vector search, and LLM integration for building intelligent document assistants.

## Features

* PDF document upload and processing
* Text chunking and embedding generation
* Vector search using Qdrant
* Retrieval-Augmented Generation (RAG)
* Multi-provider LLM support
* Source-based answer generation
* Streamlit user interface
* FastAPI backend services

## Tech Stack

* Python
* FastAPI
* Streamlit
* Qdrant
* OpenAI / Gemini / Claude
* Ollama
* Pydantic

## How It Works

1. Users upload PDF documents.
2. Documents are divided into smaller text chunks.
3. Embeddings are generated for each chunk.
4. Embeddings are stored in Qdrant.
5. User questions are converted into embeddings.
6. Relevant document sections are retrieved.
7. The LLM generates answers using the retrieved context.

## Project Structure

```text
rag-engine/
│
├── main.py
├── streamlit_app.py
├── data_loader.py
├── vector_db.py
├── custom_types.py
├── uploads/
├── qdrant_storage/
├── rag-engine/
├── tests/
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd rag-engine

pip install -r requirements.txt
```

## Run the Project

### Start the FastAPI Backend

```bash
uvicorn main:app --reload
```

### Start the Streamlit Interface

```bash
streamlit run streamlit_app.py
```

The application will be available at:

```text
http://localhost:8501
```

## Example Use Cases

* Document question answering
* Knowledge base assistant
* Research document exploration
* Internal company documentation search

## Learning Outcomes

Through this project, I learned:

* Retrieval-Augmented Generation (RAG)
* Vector databases and embeddings
* Document processing pipelines
* FastAPI backend development
* Streamlit application development
* LLM integration and prompt engineering

## Future Improvements

* Support for additional document formats
* Conversation memory
* Improved retrieval and reranking
* User authentication
* Cloud deployment support

## License

This project is based on open-source code released under the MIT License.
Original copyright belongs to the respective author.
I have used this project for learning, documentation, and portfolio-building purposes.
