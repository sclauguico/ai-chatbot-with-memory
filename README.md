# AI Chatbot with Memory

A simple chatbot implementation using LangChain, Ollama, and PostgreSQL for conversation memory.

## Setup Instructions

1. Install Ollama: https://ollama.ai/
2. Pull a model: `ollama pull llama2:7b-chat`
3. Install Python dependencies: `pip install -r requirements.txt`
4. Start PostgreSQL: `docker-compose up -d`
5. Run the app: `streamlit run frontend/app.py`

## Features

- Offline LLM using Ollama
- Persistent conversation memory with PostgreSQL
- Simple web interface with Streamlit

See [project_document.ipynb](https://github.com/sclauguico/ai-chatbot-assessment/tree/main/notebook) for full technical guide