# RAG Document Q&A System

A Retrieval-Augmented Generation (RAG) based document question-answering system built with LangChain, FAISS, and Streamlit.

## Features

- 📄 **Multi-format Support**: Upload PDF, DOCX, and TXT documents
- 🔍 **Semantic Search**: FAISS-powered vector similarity search
- 💬 **Conversational**: Multi-turn dialogue with memory
- 📊 **Source Citations**: Responses include document references
- 🎯 **Configurable**: Adjustable chunking and retrieval parameters

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | LangChain 1.2.x |
| LLM | GPT-4o-mini (via OpenRouter) |
| Embeddings | text-embedding-3-small |
| Vector Store | FAISS (local) |
| UI | Streamlit |
| Config | Pydantic Settings |

## Quick Start

### 1. Clone & Setup Environment

```bash
# Clone repository
git clone https://github.com/insetavijit/lang-chain-rag-2.git
cd lang-chain-rag-2

# Create virtual environment with uv
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
uv sync
```

### 2. Configure API Keys

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
```

### 3. Run the Application

```bash
streamlit run app.py
```

## Project Structure

```
lang-chain-rag-2/
├── src/                  # Core modules
│   ├── config.py         # Settings & environment
│   ├── loaders.py        # Document loaders
│   ├── chunker.py        # Text splitting
│   ├── embeddings.py     # Embedding generation
│   ├── vectorstore.py    # FAISS operations
│   ├── chain.py          # RAG chain
│   └── memory.py         # Conversation memory
├── app.py                # Streamlit entry point
├── notebooks/            # Jupyter notebooks
├── data/                 # Documents & vector store
└── tests/                # Test files
```

## Configuration

All settings are managed via environment variables. See `.env.example` for available options.

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | - |
| `LLM_MODEL` | Model for generation | `gpt-4o-mini` |
| `EMBEDDING_MODEL` | Model for embeddings | `text-embedding-3-small` |
| `CHUNK_SIZE` | Tokens per chunk | `800` |
| `CHUNK_OVERLAP` | Overlap between chunks | `200` |
| `RETRIEVAL_K` | Documents to retrieve | `4` |

## Development

```bash
# Install dev dependencies
uv sync --extra dev

# Run tests
pytest tests/

# Format code
black src/ tests/
ruff check src/ tests/
```

## License

MIT License - see [LICENSE](LICENSE) for details.
