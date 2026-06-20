# Customer Support Chatbot using RAG

## Overview

This project is an AI-powered customer support chatbot built using Retrieval-Augmented Generation (RAG). The chatbot answers user questions by retrieving relevant information from a knowledge base and using a Large Language Model (LLM) to generate responses.

The goal of this project is to improve response accuracy and reduce hallucinations by grounding answers in provided documents.

## Features

* Document-based question answering
* Retrieval-Augmented Generation (RAG)
* Semantic search using vector embeddings
* Conversation history support
* Source-aware responses
* FastAPI backend
* Easy document ingestion and indexing

## Tech Stack

* Python
* FastAPI
* OpenAI API
* ChromaDB / FAISS
* LangChain
* Docker

## How It Works

1. Documents are uploaded and processed.
2. Text is divided into smaller chunks.
3. Embeddings are created and stored in a vector database.
4. User queries are converted into embeddings.
5. Relevant document chunks are retrieved.
6. The retrieved context is sent to the LLM.
7. The chatbot generates a response based on the retrieved information.

## Project Structure

```text
customer-support-chatbot/
│
├── data/
├── src/
├── scripts/
├── tests/
├── configs/
├── Dockerfile
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd customer-support-chatbot

pip install -r requirements.txt
```

## Run the Project

```bash
uvicorn src.api.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

## Example Use Cases

* FAQ chatbot
* Customer support automation
* Company knowledge assistant
* Internal documentation search

## Learning Outcomes

Through this project, I learned:

* Retrieval-Augmented Generation (RAG)
* Prompt Engineering
* Vector Databases
* FastAPI Development
* LLM Application Development
* Document Processing Pipelines

## Future Improvements

* Multi-language support
* Better reranking techniques
* User authentication
* Feedback-based response improvement
* Advanced evaluation metrics

## License

This project is based on open-source code released under the MIT License.  
Original copyright belongs to the respective author.  
I have used this project for learning, documentation, and portfolio-building purposes.
