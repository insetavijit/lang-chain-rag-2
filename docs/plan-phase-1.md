# Phase 1: Project Setup & Planning - Implementation Plan

**Duration**: 2 days | **Goal**: Establish development environment and architecture

---

## 1. Create GitHub Repository

### Best Practices

| Practice | Recommendation |
|----------|----------------|
| Repository naming | Use kebab-case: `rag-document-qa` |
| Visibility | Public (for portfolio) or Private (if using proprietary data) |
| License | MIT or Apache 2.0 for open-source projects |
| Branch strategy | `main` for production, `develop` for active development |

### Repository Structure (Intermediate)

**Philosophy**: Organized with `src/` folder but keeping files flat within logical groups.

```
rag-document-qa/
│
├── .env                      # API keys (gitignored)
├── .env.example              # Template for environment variables
├── .gitignore                # Python + IDE ignores
├── README.md                 # Project documentation
├── pyproject.toml            # Dependencies & project config
│
├── src/                      # All source code
│   ├── __init__.py
│   ├── config.py             # Settings & environment loading
│   ├── loaders.py            # Document loaders (PDF, DOCX, TXT)
│   ├── chunker.py            # Text splitting logic
│   ├── embeddings.py         # Embedding generation
│   ├── vectorstore.py        # FAISS vector store operations
│   ├── chain.py              # RAG chain & retrieval logic
│   └── memory.py             # Conversation memory
│
├── app.py                    # Main Streamlit application (entry point)
│
├── notebooks/                # Jupyter notebooks
│   ├── 01_exploration.ipynb  # API testing & experiments
│   └── 02_rag_testing.ipynb  # RAG chain development
│
├── data/                     # Data storage (gitignored)
│   ├── documents/            # Uploaded documents
│   └── vectorstore/          # Persisted FAISS index
│
└── tests/                    # Test files
    ├── __init__.py
    └── test_chain.py         # Start with one test file
```

**Total: ~15 files + 4 folders** — Organized but not overwhelming!

---

### Structure Rationale

| Folder/File | Purpose |
|-------------|---------|
| `src/` | All core logic in one place, easy imports |
| `app.py` | Entry point at root for easy `streamlit run app.py` |
| `notebooks/` | Interactive development & experimentation |
| `data/` | Uploaded files & vector store persistence |
| `tests/` | Ready for testing when needed |

### Import Pattern

With this structure, imports are clean:

```python
# In app.py
from src.config import settings
from src.loaders import load_document
from src.chain import create_rag_chain

# In src/chain.py
from src.embeddings import get_embeddings
from src.vectorstore import get_vectorstore
```

### Essential `.gitignore` Contents

```gitignore
# Environment
.env
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# Data (large files)
data/documents/
data/vector_store/
*.pdf
*.docx

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

## 2. Setup Python Environment

### Option A: Using `uv` (Recommended - Faster)

```bash
# Install uv (if not installed)
pip install uv

# Create project with uv
uv init rag-document-qa
cd rag-document-qa

# Create virtual environment
uv venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate
```

### Option B: Using `pip` + `venv`

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `langchain` | ^1.2.x | Core framework for RAG chains |
| `langchain-openai` | ^1.1.x | OpenAI integrations |
| `langchain-community` | ^0.3.x | Community integrations (loaders, etc.) |
| `openai` | ^2.15.x | OpenAI API client |
| `faiss-cpu` | ^1.13.x | Vector similarity search |
| `streamlit` | ^1.52.x | Web interface |
| `python-dotenv` | ^1.0.x | Environment variable management |
| `pypdf` | ^6.6.x | PDF document loading |
| `python-docx` | ^1.x | DOCX document loading |
| `tiktoken` | ^0.7.x | Token counting for chunking |
| `jupyter` | ^1.0.x | Jupyter Notebook support |
| `ipykernel` | ^6.29.x | Python kernel for Jupyter |
| `ipywidgets` | ^8.1.x | Interactive widgets for notebooks |

### `requirements.txt`

```txt
# Core LangChain
langchain>=1.2.0
langchain-openai>=1.1.0
langchain-community>=0.3.0

# LLM & Embeddings
openai>=2.15.0
tiktoken>=0.7.0

# Vector Store
faiss-cpu>=1.13.0

# Document Loaders
pypdf>=6.6.0
python-docx>=1.0.0
unstructured>=0.10.0

# Web Interface
streamlit>=1.52.0

# Utilities
python-dotenv>=1.0.0
pydantic>=2.0.0
pydantic-settings>=2.12.0

# Jupyter Notebook Support
jupyter>=1.0.0
ipykernel>=6.29.0
ipywidgets>=8.1.0
notebook>=7.0.0

# Development
pytest>=8.0.0
black>=24.0.0
ruff>=0.1.0
```

### `pyproject.toml` (for uv/poetry)

```toml
[project]
name = "rag-document-qa"
version = "0.1.0"
description = "RAG-based Document Q&A System using LangChain"
requires-python = ">=3.10"
readme = "README.md"
license = { text = "MIT" }

dependencies = [
    "langchain>=1.2.0",
    "langchain-openai>=1.1.0",
    "langchain-community>=0.3.0",
    "openai>=2.15.0",
    "faiss-cpu>=1.13.0",
    "streamlit>=1.52.0",
    "python-dotenv>=1.0.0",
    "pypdf>=6.6.0",
    "python-docx>=1.0.0",
    "tiktoken>=0.7.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.12.0",
    "jupyter>=1.0.0",
    "ipykernel>=6.29.0",
    "ipywidgets>=8.1.0",
    "notebook>=7.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "black>=24.0.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.black]
line-length = 88
target-version = ["py310"]
```

---

## 3. Configure API Keys

### Required API Keys

| Provider | Key Name | Purpose | Free Tier |
|----------|----------|---------|-----------|
| OpenAI | `OPENAI_API_KEY` | GPT-4o-mini + Embeddings | $5 credit (new accounts) |
| **OR** OpenRouter | `OPENROUTER_API_KEY` | Multi-model access | Pay-as-you-go |
| **OR** Groq | `GROQ_API_KEY` | Fast inference (Llama, Mixtral) | Free tier available |
| HuggingFace | `HUGGINGFACE_API_KEY` | Alternative embeddings | Free |
| Langfuse (Optional) | `LANGFUSE_*` | Tracing & observability | Free tier |

### `.env` File Structure

```env
# ===========================================
# LLM Provider (choose one or more)
# ===========================================

# Option 1: OpenRouter (multi-model access - RECOMMENDED)
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Option 2: Groq (fast & free tier)
GROQ_API_KEY=gsk_your-key-here

# Option 3: OpenAI (direct access)
# OPENAI_API_KEY=sk-...

# ===========================================
# Observability & Tracing (Langfuse)
# ===========================================

LANGFUSE_SECRET_KEY=sk-lf-your-secret-key
LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key
LANGFUSE_BASE_URL=https://cloud.langfuse.com

# ===========================================
# Application Settings
# ===========================================

# Model Configuration
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# RAG Settings
CHUNK_SIZE=800
CHUNK_OVERLAP=200
RETRIEVAL_K=4
```

### `.env.example` (Commit this to Git)

```env
# Copy this file to .env and fill in your values
# DO NOT commit .env to version control!

# LLM Provider (OpenRouter recommended for multi-model access)
OPENROUTER_API_KEY=your-openrouter-key-here

# Alternative: Groq (free tier available)
GROQ_API_KEY=your-groq-key-here

# Langfuse Tracing (get keys from https://cloud.langfuse.com)
LANGFUSE_SECRET_KEY=sk-lf-your-secret-key
LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key
LANGFUSE_BASE_URL=https://cloud.langfuse.com

# Model Configuration
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# RAG Settings
CHUNK_SIZE=800
CHUNK_OVERLAP=200
RETRIEVAL_K=4
```

### Configuration Management (`src/config/settings.py`)

```python
"""
Application configuration using Pydantic Settings.
Loads environment variables with validation and defaults.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # LLM Provider Keys (at least one required)
    openrouter_api_key: Optional[str] = Field(default=None)
    groq_api_key: Optional[str] = Field(default=None)
    openai_api_key: Optional[str] = Field(default=None)
    
    # Langfuse Tracing
    langfuse_secret_key: Optional[str] = Field(default=None)
    langfuse_public_key: Optional[str] = Field(default=None)
    langfuse_base_url: str = Field(default="https://cloud.langfuse.com")
    
    # Model Configuration
    llm_model: str = Field(default="gpt-4o-mini")
    embedding_model: str = Field(default="text-embedding-3-small")
    
    # RAG Settings
    chunk_size: int = Field(default=800)
    chunk_overlap: int = Field(default=200)
    retrieval_k: int = Field(default=4)
    
    # Paths
    data_dir: str = Field(default="data")
    vector_store_path: str = Field(default="data/vector_store")
    
    # Langfuse (Optional)
    langfuse_public_key: Optional[str] = Field(default=None)
    langfuse_secret_key: Optional[str] = Field(default=None)
    langfuse_host: str = Field(default="https://cloud.langfuse.com")
    
    def get_active_llm_provider(self) -> str:
        """Determine which LLM provider to use based on available keys."""
        if self.openrouter_api_key:
            return "openrouter"
        elif self.groq_api_key:
            return "groq"
        elif self.openai_api_key:
            return "openai"
        else:
            raise ValueError("No LLM API key configured. Set OPENROUTER_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY.")


# Singleton instance
settings = Settings()
```

---

## 3.1 Jupyter Notebook Setup

### Register Kernel with Virtual Environment

After installing dependencies, register your virtual environment as a Jupyter kernel:

```bash
# Activate virtual environment first
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # macOS/Linux

# Register kernel
python -m ipykernel install --user --name=rag-document-qa --display-name="RAG Document QA"
```

### VS Code Jupyter Configuration

Add to `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
    "jupyter.notebookFileRoot": "${workspaceFolder}",
    "notebook.cellToolbarLocation": {
        "default": "right",
        "jupyter-notebook": "left"
    },
    "jupyter.widgetScriptSources": ["jsdelivr.com", "unpkg.com"],
    "notebook.output.wordWrap": true,
    "notebook.lineNumbers": "on"
}
```

### Create Exploration Notebook

Create `notebooks/01_exploration.ipynb` for interactive development:

```python
# Cell 1: Load environment
from dotenv import load_dotenv
import os

load_dotenv()
print(f"OpenRouter API Key: {'✓ Set' if os.getenv('OPENROUTER_API_KEY') else '✗ Missing'}")
print(f"Groq API Key: {'✓ Set' if os.getenv('GROQ_API_KEY') else '✗ Missing'}")
print(f"Langfuse Keys: {'✓ Set' if os.getenv('LANGFUSE_SECRET_KEY') else '✗ Missing'}")
```

```python
# Cell 2: Test LLM Connection
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

response = llm.invoke("Hello! Say 'RAG system ready!' if you can hear me.")
print(response.content)
```

### Notebook Directory Structure

Start with two notebooks for development:

```
notebooks/
├── 01_exploration.ipynb  # API testing & experiments
└── 02_rag_testing.ipynb  # RAG chain development
```

**Add more notebooks as you progress:**
- `03_document_loading.ipynb` — When testing different file types
- `04_evaluation.ipynb` — When working on Phase 5

---

## 4. Design System Architecture

### High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RAG Document Q&A System                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │   Document   │    │    Text      │    │   Embedding  │    │   Vector  │ │
│  │   Upload     │───▶│   Chunking   │───▶│  Generation  │───▶│   Store   │ │
│  │  (PDF/DOCX)  │    │  (800 tokens)│    │(embed-3-sm)  │    │  (FAISS)  │ │
│  └──────────────┘    └──────────────┘    └──────────────┘    └─────┬─────┘ │
│                                                                     │       │
│  ┌──────────────────────────────────────────────────────────────────┴─────┐ │
│  │                         Query Processing                               │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                        │ │
│  │  ┌───────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────┐ │ │
│  │  │   User    │    │    Query     │    │  Similarity  │    │   LLM   │ │ │
│  │  │  Question │───▶│  Embedding   │───▶│   Search     │───▶│ Response│ │ │
│  │  │           │    │              │    │   (top-k=4)  │    │(4o-mini)│ │ │
│  │  └───────────┘    └──────────────┘    └──────────────┘    └────┬────┘ │ │
│  │                                                                 │      │ │
│  └─────────────────────────────────────────────────────────────────┼──────┘ │
│                                                                     │       │
│  ┌──────────────────────────────────────────────────────────────────▼─────┐ │
│  │                        Response Generation                             │ │
│  │  • Answer with source citations                                        │ │
│  │  • Conversation memory (multi-turn)                                    │ │
│  │  • Metadata (document name, page number)                               │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI Layer                       │
│  ┌─────────────┐  ┌─────────────────┐  ┌─────────────────────┐ │
│  │   Upload    │  │  Chat Interface │  │     Settings        │ │
│  │    Page     │  │      Page       │  │       Page          │ │
│  └──────┬──────┘  └────────┬────────┘  └──────────┬──────────┘ │
└─────────┼──────────────────┼─────────────────────┼─────────────┘
          │                  │                     │
          ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Service Layer                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Document      │  │    RAG Chain    │  │   Config        │ │
│  │   Processor     │  │    Service      │  │   Manager       │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
└───────────┼────────────────────┼────────────────────┼──────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Core Components                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────┐ │
│  │ Document │ │   Text   │ │Embedding │ │  Vector  │ │  LLM  │ │
│  │ Loaders  │ │ Chunker  │ │Generator │ │  Store   │ │Client │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └───┬───┘ │
└───────┼────────────┼────────────┼────────────┼───────────┼─────┘
        │            │            │            │           │
        ▼            ▼            ▼            ▼           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     External Services                           │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐│
│  │  File System │  │  OpenAI API  │  │  FAISS (Local Index)   ││
│  └──────────────┘  └──────────────┘  └────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### Create Architecture Documentation (`docs/ARCHITECTURE.md`)

This document should be created with detailed explanations of:
- System components and their responsibilities
- Data flow diagrams
- API contracts between components
- Error handling strategies
- Scalability considerations

---

## 5. Select Tech Stack

### Final Technology Decisions

| Category | Choice | Rationale |
|----------|--------|-----------|
| **Language** | Python 3.10+ | LangChain ecosystem, ML libraries |
| **Framework** | LangChain 1.2.x | Industry standard for RAG, active development |
| **LLM** | GPT-4o-mini | Best cost/quality ratio, 128K context, multimodal |
| **Embeddings** | text-embedding-3-small | 5x cheaper than ada-002, better performance |
| **Vector DB** | FAISS (local) | No setup required, performant for <1M vectors |
| **UI** | Streamlit | Rapid development, built-in components |
| **Config** | Pydantic Settings | Type-safe, validation, .env support |

### Alternative Options (For Stretch Goals)

| Category | Alternative | When to Use |
|----------|-------------|-------------|
| **LLM** | GPT-4o | Better reasoning, vision capabilities |
| **LLM** | Claude 3.5 Sonnet (via OpenRouter) | Long context, excellent instruction following |
| **LLM** | Llama 3.3 (via Groq) | Free tier, fast inference |
| **Embeddings** | text-embedding-3-large | Higher accuracy, 256-3072 dims |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) | Free, local, smaller vectors |
| **Vector DB** | Chroma | Persistent, metadata filtering |
| **Vector DB** | Pinecone | Cloud-hosted, managed, scalable |
| **UI** | Gradio | Alternative to Streamlit |

---

## Phase 1 Checklist

- [ ] **Repository Setup**
  - [ ] Create GitHub repository
  - [ ] Initialize with README, .gitignore, LICENSE
  - [ ] Create folder structure as documented
  - [ ] Set up branch protection (optional)

- [ ] **Python Environment**
  - [ ] Install Python 3.10+
  - [ ] Create virtual environment (uv or venv)
  - [ ] Install core dependencies
  - [ ] Verify installations with import tests

- [ ] **API Configuration**
  - [ ] Obtain API key (OpenAI/OpenRouter/Groq)
  - [ ] Create .env file with keys
  - [ ] Create .env.example template
  - [ ] Implement settings.py configuration

- [ ] **Architecture**
  - [ ] Create docs/ARCHITECTURE.md
  - [ ] Document data flow diagrams
  - [ ] Define component interfaces
  - [ ] Plan error handling strategy

- [ ] **Verification**
  - [ ] Run simple API test (LLM call)
  - [ ] Verify all imports work
  - [ ] Test configuration loading
  - [ ] Commit initial project structure

---

## Phase 1 Completion Criteria

✅ Virtual environment created and activated  
✅ All dependencies installed without errors  
✅ API key configured and validated  
✅ Project structure matches architecture  
✅ Configuration loading works correctly  
✅ Simple "Hello World" LLM call succeeds  
✅ Code committed to GitHub repository  

---

## Next Steps → Phase 2

Once Phase 1 is complete, proceed to **Phase 2: Document Processing Pipeline** where you will:

1. Implement document loaders for PDF, DOCX, and TXT files
2. Build the text chunking pipeline with RecursiveCharacterTextSplitter
3. Create embedding generation functions
4. Set up FAISS vector store with persistence

---

*Document created: 2026-01-11 | Last updated: 2026-01-11*
