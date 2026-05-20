# Advanced Context-Aware Enterprise RAG Chatbot Engine

A production-ready, full-stack Retrieval-Augmented Generation (RAG) chatbot application. This project architectures a high-performance **FastAPI** backend coupled with a local **ChromaDB** vector storage cluster to index, embed, and query custom proprietary documentation using advanced Large Language Models (LLMs).

## 🚀 Key Features & Architecture Highlights
* **Decoupled Architecture:** Clean separation of concerns between an asynchronous API Backend server (FastAPI) and a rapid-rendering presentation UI (Streamlit).
* **Semantic Retrieval Pipeline:** Fully local document indexing engine powered by ChromaDB persistent vector stores utilizing semantic vector lookups.
* **Hallucination Mitigation:** Implemented a secure prompt synthesis pipeline that enforces rigid contextual guardrails via targeted system instructions.
* **Secure Enterprise Secrets Management:** Employs zero-string-hardcoding environment variable routing to safeguard model API credentials against operational leaks.

---

## 🛠️ Tech Stack & Dependencies
* **Core Language:** Python 3.10+
* **Backend Framework:** FastAPI, Uvicorn
* **Frontend Web App:** Streamlit
* **Vector Database:** ChromaDB
* **AI Core Orchestration:** Google GenAI SDK (`gemini-2.5-flash`, `gemini-embedding-2`)

---

## 📦 Project Workspace Topology
```text
advanced-ai-chatbot/
│
├── backend/
│   ├── main.py          # FastAPI server routes & prompt synthesis
│   └── database.py      # ChromaDB storage logic & vector embeddings
│
├── frontend/
│   └── app.py           # Streamlit interface & stateful chat logic
│
├── documents/           # Directory for proprietary text files/PDF inputs
├── .gitignore           # Safeguards local vector logs and environment tokens
└── requirements.txt     # System package manifests
