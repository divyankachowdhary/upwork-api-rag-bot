# Upwork API RAG Bot

A retrieval-augmented chatbot that answers developer questions about the Upwork API, grounded only in the official API documentation. If the docs don't cover something, the bot says so instead of guessing.

# Stack: Streamlit · LangChain · ChromaDB · bge-small-en-v1.5 embeddings · Llama 3.1 8B via Groq

# How it works
1. The Upwork API documentation PDF is parsed (tables included), chunked, embedded, and stored in a local Chroma vector index.
2. Each question is embedded and matched against the top candidate chunks, which are then re-ranked using a set of heuristics (endpoint      detection, parameter tables, grant types, etc.) before the top 5 are kept.
3. Those chunks are passed to the LLM with a prompt that forces it into one of four response modes: small talk, direct answer, answer-by-    inference, or "not covered in the docs" — so it never invents endpoints, scopes, or rate limits that aren't actually there.


# Setup 
requires uv 
uv sync                          # install dependencies into .venv
cp .env.example .env             # then add your Groq API key
uv run python -m src.ingest      # build the vector index from the PDF
uv run streamlit run app.py      # launch the chat UI
