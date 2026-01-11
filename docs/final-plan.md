# Building a RAG Document Q&A System: Phase 1 Implementation Guide

*A comprehensive guide to setting up your development environment and project architecture*

**Duration**: 2 days | **Goal**: Establish development environment and architecture

---

## Introduction

This document serves as your complete roadmap for establishing the foundation of a Retrieval-Augmented Generation (RAG) Document Q&A System. Over the course of approximately two days, you will transform an empty directory into a fully configured development environment, complete with all the tools, dependencies, and architectural decisions needed to build an intelligent document question-answering application.

RAG represents one of the most practical applications of Large Language Models (LLMs) in production environments. By combining the power of vector similarity search with the reasoning capabilities of modern LLMs, RAG systems can provide accurate, contextually-grounded answers based on your own documents. This phase focuses entirely on laying the groundwork—because a solid foundation is essential for the development work that follows.

By the end of Phase 1, you will have a working development environment where you can make a successful API call to an LLM, a well-organized project structure ready for implementation, and a clear understanding of the architecture you'll be building.

---

## Part 1: Version Control & Repository Setup

### Why Version Control Matters

Before writing a single line of code, establishing version control is essential. Git provides not only a safety net for your work but also creates a professional portfolio piece that demonstrates your capabilities to potential employers or collaborators. A well-structured repository tells a story about your development practices and attention to detail.

### Repository Best Practices

| Practice | Recommendation |
|----------|----------------|
| Repository naming | Use kebab-case: `rag-document-qa` |
| Visibility | Public (for portfolio) or Private (if using proprietary data) |
| License | MIT or Apache 2.0 for open-source projects |
| Branch strategy | `main` for production, `develop` for active development |

### The Intermediate Project Structure

The project structure strikes a balance between simplicity and organization. Rather than starting with a deeply nested hierarchy that may feel overwhelming, or a completely flat structure that becomes unwieldy as the project grows, this intermediate approach groups related functionality while keeping navigation intuitive.

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

### Understanding the Structure

The structure centers around a `src/` directory that houses all core application logic. This separation keeps the root directory clean while making imports predictable and consistent. The main entry point, `app.py`, sits at the root level for convenient execution—you'll simply run `streamlit run app.py` to launch the application.

| Folder/File | Purpose |
|-------------|---------|
| `src/` | All core logic in one place, easy imports |
| `app.py` | Entry point at root for easy `streamlit run app.py` |
| `notebooks/` | Interactive development & experimentation |
| `data/` | Uploaded files & vector store persistence |
| `tests/` | Ready for testing when needed |

Within the `src/` directory, each file corresponds to a distinct responsibility in the RAG pipeline:

- **config.py** handles all settings and environment variable loading, ensuring your application has a single source of truth for configuration
- **loaders.py** manages document ingestion, supporting PDF, DOCX, and plain text files
- **chunker.py** implements the text splitting logic that breaks documents into manageable pieces
- **embeddings.py** generates vector representations of text for similarity search
- **vectorstore.py** handles all interactions with the FAISS vector database
- **chain.py** orchestrates the RAG pipeline, connecting retrieval with generation
- **memory.py** maintains conversation context for multi-turn dialogues

### Import Patterns

With this structure, imports become clean and predictable:

```python
# In app.py
from src.config import settings
from src.loaders import load_document
from src.chain import create_rag_chain

# In src/chain.py
from src.embeddings import get_embeddings
from src.vectorstore import get_vectorstore
```

This consistency reduces cognitive load and makes the codebase more accessible to collaborators—or to yourself when you return to the code after time away.

### Essential .gitignore

Your `.gitignore` file prevents sensitive data and large files from being committed:

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

## Part 2: Python Environment Configuration

### Choosing Your Tools

Python's ecosystem offers several approaches to dependency management. This guide recommends `uv`, a modern package manager that offers significantly faster installation times compared to traditional pip. However, the familiar `pip` + `venv` combination remains a reliable alternative if you prefer established tools.

### Option A: Using UV (Recommended - Faster)

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

### Option B: Using pip + venv

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Regardless of which approach you choose, always work within a virtual environment. This isolation prevents dependency conflicts between projects and ensures reproducibility—your project will work the same way on any machine that replicates your environment.

### Core Dependencies

The dependency stack has been carefully selected to provide everything needed for a production-quality RAG system while remaining manageable in scope.

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

**LangChain** serves as the backbone of your RAG implementation. It provides abstractions for document loading, text splitting, embedding generation, vector stores, and chain composition. The framework has become an industry standard for LLM application development.

**FAISS** implements Facebook AI Similarity Search, an extremely efficient library for similarity search in high-dimensional vector spaces. The CPU version works on any machine without requiring GPU setup.

**Streamlit** enables rapid creation of web interfaces for data applications. With just Python code, you can create interactive file uploaders, chat interfaces, and visualizations.

### requirements.txt

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

### pyproject.toml (for uv/poetry)

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

## Part 3: API Configuration & Security

### Understanding Your Provider Options

The modern LLM landscape offers multiple paths to accessing powerful language models. Your choice of provider affects cost, performance, and available features.

| Provider | Key Name | Purpose | Free Tier |
|----------|----------|---------|-----------|
| OpenAI | `OPENAI_API_KEY` | GPT-4o-mini + Embeddings | $5 credit (new accounts) |
| **OR** OpenRouter | `OPENROUTER_API_KEY` | Multi-model access | Pay-as-you-go |
| **OR** Groq | `GROQ_API_KEY` | Fast inference (Llama, Mixtral) | Free tier available |
| HuggingFace | `HUGGINGFACE_API_KEY` | Alternative embeddings | Free |
| Langfuse (Optional) | `LANGFUSE_*` | Tracing & observability | Free tier |

**OpenRouter** emerges as the recommended choice for this project. It provides unified access to models from OpenAI, Anthropic, Google, Meta, and others through a single API endpoint. This flexibility allows you to experiment with different models without changing your integration code.

**Groq** offers an attractive alternative, particularly for developers seeking fast inference at minimal cost. Groq's custom hardware delivers impressively low latency, and their free tier provides substantial usage for development.

### .env File Structure

API keys represent sensitive credentials that must never appear in version control. The `.env` file pattern solves this elegantly:

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

### .env.example (Commit this to Git)

Create a template that collaborators can copy without exposing your actual credentials:

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

### Configuration Management with Pydantic

Rather than scattering environment variable access throughout your codebase, centralize configuration in a dedicated module using Pydantic Settings. This approach provides automatic environment variable loading with sensible defaults, type validation that catches configuration errors early, and a clear, self-documenting interface to your application's settings.

Create `src/config.py`:

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
    vector_store_path: str = Field(default="data/vectorstore")
    
    def get_active_llm_provider(self) -> str:
        """Determine which LLM provider to use based on available keys."""
        if self.openrouter_api_key:
            return "openrouter"
        elif self.groq_api_key:
            return "groq"
        elif self.openai_api_key:
            return "openai"
        else:
            raise ValueError(
                "No LLM API key configured. "
                "Set OPENROUTER_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY."
            )


# Singleton instance
settings = Settings()
```

The `get_active_llm_provider()` method exemplifies thoughtful configuration design—it examines which API keys are present and returns the appropriate provider identifier, allowing your application to adapt to whatever credentials are available.

---

## Part 4: Jupyter Notebook Integration

### The Role of Notebooks in Development

Jupyter notebooks serve as your laboratory for experimentation. Before committing logic to production code, you can prototype in a notebook, see immediate results, and iterate rapidly. This workflow accelerates development by providing instant feedback and visual output.

For this project, notebooks prove particularly valuable for:
- Testing API connections before building the full application
- Experimenting with chunking strategies to find optimal parameters
- Visualizing embedding spaces to understand how your documents cluster
- Debugging RAG chain behavior with step-by-step execution

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

Visual Studio Code provides excellent Jupyter support. Add to `.vscode/settings.json`:

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

Create `notebooks/01_exploration.ipynb` for interactive development. Start with cells that validate your setup:

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

## Part 5: System Architecture

### The RAG Pipeline

Understanding the RAG architecture provides essential context for implementation decisions. The system operates in two distinct phases: document ingestion and query processing.

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

**During document ingestion**, uploaded files flow through a pipeline:
1. Documents are loaded and converted to text
2. Text is split into chunks of approximately 800 tokens with 200-token overlap
3. Each chunk is converted into a vector embedding using text-embedding-3-small
4. Embeddings are indexed in the FAISS vector store for efficient retrieval

**Query processing** reverses this flow:
1. User questions are converted to embeddings using the same model
2. The vector store finds the most similar document chunks (top 4)
3. These chunks provide context for the LLM
4. GPT-4o-mini generates a response grounded in the retrieved content

### Component Architecture

The architecture organizes into distinct layers, each with clear responsibilities:

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

- The **UI Layer** (Streamlit) handles user interaction—file uploads, chat input, and response display
- The **Service Layer** contains business logic orchestration
- The **Core Components Layer** implements specific capabilities
- The **External Services Layer** represents dependencies outside your codebase

This layered architecture promotes separation of concerns, making the system easier to test, maintain, and extend.

---

## Part 6: Technology Selection

### Final Technology Decisions

Each technology choice reflects careful consideration of project requirements, learning opportunities, and production readiness.

| Category | Choice | Rationale |
|----------|--------|-----------|
| **Language** | Python 3.10+ | LangChain ecosystem, ML libraries |
| **Framework** | LangChain 1.2.x | Industry standard for RAG, active development |
| **LLM** | GPT-4o-mini | Best cost/quality ratio, 128K context, multimodal |
| **Embeddings** | text-embedding-3-small | 5x cheaper than ada-002, better performance |
| **Vector DB** | FAISS (local) | No setup required, performant for <1M vectors |
| **UI** | Streamlit | Rapid development, built-in components |
| **Config** | Pydantic Settings | Type-safe, validation, .env support |

**GPT-4o-mini** strikes the optimal balance for this project. It offers near-GPT-4 quality at a fraction of the cost, supports 128K token context windows, includes multimodal capabilities, and provides fast response times suitable for interactive applications.

**text-embedding-3-small** offers dramatically improved value compared to the older ada-002 model—approximately five times cheaper with better performance on standard benchmarks.

**FAISS** provides vector search without external infrastructure dependencies. Running locally, it eliminates network latency and external service costs while performing exceptionally well for collections under a million vectors.

### Alternative Options (For Stretch Goals)

The architecture accommodates future flexibility:

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

## Part 7: Implementation Checklist

### Repository Setup

- [ ] Create GitHub repository with documented naming conventions
- [ ] Initialize with README, .gitignore, LICENSE
- [ ] Create folder structure as documented
- [ ] Set up branch protection (optional)

### Python Environment

- [ ] Install Python 3.10+
- [ ] Create virtual environment (uv or venv)
- [ ] Install core dependencies
- [ ] Verify installations with import tests

### API Configuration

- [ ] Obtain API key (OpenRouter/Groq/OpenAI)
- [ ] Create .env file with keys
- [ ] Create .env.example template
- [ ] Implement config.py configuration module

### Jupyter Setup

- [ ] Register kernel with virtual environment
- [ ] Create VS Code settings for Jupyter
- [ ] Create exploration notebook
- [ ] Verify notebook can access dependencies

### Verification

- [ ] Run simple API test (LLM call)
- [ ] Verify all imports work
- [ ] Test configuration loading
- [ ] Commit initial project structure

---

## Phase 1 Completion Criteria

You have successfully completed Phase 1 when:

✅ Virtual environment created and activated  
✅ All dependencies installed without errors  
✅ API key configured and validated  
✅ Project structure matches architecture  
✅ Configuration loading works correctly  
✅ Simple "Hello World" LLM call succeeds  
✅ Code committed to GitHub repository  

---

## Looking Ahead: Phase 2 Preview

With your development environment established, Phase 2 will focus on the document processing pipeline—the first major component of your RAG system:

1. **Implement document loaders** for PDF, DOCX, and TXT files
2. **Build text chunking pipeline** with RecursiveCharacterTextSplitter
3. **Create embedding generation** functions
4. **Set up FAISS vector store** with persistence

These components form the foundation upon which Phase 3 will build the actual RAG chain.

---

## Conclusion

Phase 1 may seem preliminary—you haven't yet built the RAG pipeline or created the chat interface that makes the application compelling. However, the work done here determines the success of everything that follows. A well-configured environment eliminates hours of debugging mysterious import errors or dependency conflicts. A thoughtful project structure makes code navigation intuitive and collaboration frictionless. Proper API configuration and security practices prevent the embarrassing (and potentially costly) exposure of credentials.

Take the time to complete each step thoroughly. Verify that things work before moving on. When you reach the end of Phase 1 and see your first successful LLM response in your exploration notebook, you'll know that your foundation is solid and you're ready to build.

---

*Document Version: 1.0*  
*Created: January 11, 2026*  
*Last Updated: January 11, 2026*
