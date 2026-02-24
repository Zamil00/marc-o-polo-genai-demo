# AI-Powered Fashion Support Assistant (RAG System)

## Overview

This project demonstrates how Generative AI can be integrated into a fashion retail environment to support customer service operations.

The system uses a Retrieval-Augmented Generation (RAG) architecture to:

- Embed internal FAQ data
- Perform semantic search
- Generate brand-consistent responses using LLMs

## Architecture

1. FAQ Data Embedding
2. Semantic Retrieval via Cosine Similarity
3. Context-Aware LLM Response Generation

## Business Value

- Reduced response time
- Consistent brand tone
- Scalable multilingual expansion
- Lower operational workload

## Tech Stack

- Python
- OpenAI API
- Embeddings (text-embedding-3-small)
- GPT-4o-mini
- NumPy

## Setup

1. Create virtual environment:
   python -m venv venv
   source venv/bin/activate  (Mac)
   venv\Scripts\activate   (Windows)

2. Install dependencies:
   pip install -r requirements.txt

3. Create .env file and add your OpenAI API key.

4. Run:
   python rag_support/main.py
