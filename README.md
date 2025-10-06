# 🚀 LLM-Powered Job Application Feedback SaaS (RAG-based Resume Optimizer)

A production-ready MVP that uses a **Retrieval-Augmented Generation (RAG)** pipeline to analyze a user’s **resume and job description**, generating personalized, actionable feedback — including tailored resume edits, interview questions, and cover-letter suggestions.


## 🧠 Project Overview
This project demonstrates a **full-stack AI SaaS architecture** built with **Next.js (TypeScript)** and **FastAPI (Python)**.  
It integrates an **LLM pipeline**, **vector database retrieval**, and **modern deployment practices**, designed to showcase real-world software engineering skills for job applications.

### ✨ Core Features
- **RAG Pipeline**: Embeds resume and job description, retrieves relevant context, and feeds it to an LLM for non-hallucinated, context-aware feedback.
- **AI Feedback Engine**: Generates actionable resume improvements, interview questions, and cover-letter bullet points.
- **Full-Stack SaaS Architecture**: Next.js frontend, FastAPI backend, vector DB integration, and API communication.
- **Authentication (Stub)**: GitHub login simulation with `next-auth`.
- **Dashboard (MVP)**: View and manage previous analyses (stored locally or in-memory).
- **Cloud Deployment**: Frontend deployed on **Vercel**, backend on **Render/Railway/AWS ECS**.
- **Scalable & Modular**: Ready for expansion into production-grade SaaS with payments and analytics.


## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | Next.js (TypeScript), Tailwind CSS, next-auth |
| **Backend** | FastAPI (Python), Uvicorn |
| **LLM / AI** | OpenAI GPT-4 or Mistral via API |
| **Embeddings** | sentence-transformers / OpenAI Embeddings |
| **Vector Database** | Qdrant / Pinecone |
| **Infrastructure** | Docker, Railway / Render / AWS ECS, Vercel |
| **Version Control & CI/CD** | GitHub + GitHub Actions |


## 🧱 System Architecture

User
│
▼
Frontend (Next.js)
│ REST API call (resume_text, job_description)
▼
Backend (FastAPI)
│ ├── Embed resume & JD → store/retrieve vectors (Qdrant)
│ ├── RAG pipeline → retrieve context
│ └── Call LLM → generate structured feedback
▼
Response → Frontend display

