# Configuration Module: Complete Guide

*Centralized settings management using Pydantic*

**File**: `src/config.py` | **Purpose**: Environment-based configuration with validation

---

## Introduction

The `config.py` module serves as the single source of truth for all application settings. Using Pydantic Settings, it provides type-safe configuration loading from environment variables with sensible defaults. This centralized approach eliminates scattered environment variable access throughout the codebase and ensures configuration errors are caught early.

---

## Part 1: Module Imports

### Dependencies

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import os
```

| Import | Purpose |
|--------|---------|
| `BaseSettings` | Base class for settings that auto-loads from environment |
| `SettingsConfigDict` | Configuration for how settings are loaded |
| `Field` | Define field defaults and validation |
| `Optional` | Type hint for nullable values |
| `os` | Standard library (available but not used directly) |

---

## Part 2: Settings Class Definition

### Class Structure

```python
class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
```

### Configuration Options

| Option | Value | Effect |
|--------|-------|--------|
| `env_file` | ".env" | Loads variables from .env file |
| `env_file_encoding` | "utf-8" | Handles special characters properly |
| `case_sensitive` | False | `OPENAI_API_KEY` = `openai_api_key` |
| `extra` | "ignore" | Ignores unknown environment variables |

### Why Pydantic Settings?

```
┌─────────────────────────────────────────────────────────────────┐
│                Traditional Approach (Scattered)                  │
├─────────────────────────────────────────────────────────────────┤
│  # In chain.py                                                   │
│  api_key = os.getenv("OPENAI_API_KEY")                          │
│                                                                  │
│  # In vectorstore.py                                             │
│  path = os.getenv("VECTOR_STORE_PATH", "default/path")          │
│                                                                  │
│  # In app.py                                                     │
│  chunk_size = int(os.getenv("CHUNK_SIZE", "800"))               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Pydantic Approach (Centralized)                 │
├─────────────────────────────────────────────────────────────────┤
│  # In any file                                                   │
│  from src.config import settings                                 │
│                                                                  │
│  settings.openai_api_key    # Type: Optional[str]               │
│  settings.vector_store_path  # Type: str                        │
│  settings.chunk_size         # Type: int                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 3: LLM Provider Configuration

### API Key Fields

```python
# LLM Provider Keys (at least one required)
openrouter_api_key: Optional[str] = Field(default=None)
groq_api_key: Optional[str] = Field(default=None)
openai_api_key: Optional[str] = Field(default=None)
```

### Provider Hierarchy

| Priority | Provider | Environment Variable |
|----------|----------|---------------------|
| 1 | OpenRouter | `OPENROUTER_API_KEY` |
| 2 | Groq | `GROQ_API_KEY` |
| 3 | OpenAI | `OPENAI_API_KEY` |

The application checks for keys in this order and uses the first available provider.

---

## Part 4: Observability Configuration

### Langfuse Tracing

```python
# Langfuse Tracing
langfuse_secret_key: Optional[str] = Field(default=None)
langfuse_public_key: Optional[str] = Field(default=None)
langfuse_base_url: str = Field(default="https://cloud.langfuse.com")
```

| Setting | Default | Purpose |
|---------|---------|---------|
| `langfuse_secret_key` | None | Private key for Langfuse API |
| `langfuse_public_key` | None | Public key for Langfuse API |
| `langfuse_base_url` | cloud.langfuse.com | Langfuse server URL |

---

## Part 5: Model Configuration

### LLM and Embedding Settings

```python
# Model Configuration
llm_model: str = Field(default="gpt-4o-mini")
embedding_model: str = Field(default="text-embedding-3-small")
```

| Setting | Default | Options |
|---------|---------|---------|
| `llm_model` | gpt-4o-mini | Any OpenAI-compatible model |
| `embedding_model` | text-embedding-3-small | OpenAI embedding models |

---

## Part 6: RAG Settings

### Retrieval Parameters

```python
# RAG Settings
chunk_size: int = Field(default=800)
chunk_overlap: int = Field(default=200)
retrieval_k: int = Field(default=4)
```

| Setting | Default | Purpose |
|---------|---------|---------|
| `chunk_size` | 800 | Maximum characters per chunk |
| `chunk_overlap` | 200 | Overlap between adjacent chunks |
| `retrieval_k` | 4 | Number of chunks to retrieve |

### Chunking Visualization

```
Document: "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."

chunk_size=800, chunk_overlap=200:

┌────────────────────────────────────────┐
│              Chunk 1 (800 chars)       │
│████████████████████████████████████████│
└────────────────────────────────────────┘
                    ┌────────────────────────────────────────┐
                    │              Chunk 2 (800 chars)       │
        ◄──────────►│████████████████████████████████████████│
         200 chars  └────────────────────────────────────────┘
         overlap
```

---

## Part 7: Path Configuration

### Data Directories

```python
# Paths
data_dir: str = Field(default="data")
vector_store_path: str = Field(default="data/vectorstore")
```

| Path | Default | Contains |
|------|---------|----------|
| `data_dir` | data/ | All application data |
| `vector_store_path` | data/vectorstore/ | FAISS index files |

---

## Part 8: Provider Detection Method

### get_active_llm_provider()

```python
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
```

### Decision Flow

```
┌─────────────────────────────────────────┐
│      get_active_llm_provider()          │
├─────────────────────────────────────────┤
│                                         │
│  OPENROUTER_API_KEY set?                │
│       ├── Yes → return "openrouter"     │
│       └── No ↓                          │
│                                         │
│  GROQ_API_KEY set?                      │
│       ├── Yes → return "groq"           │
│       └── No ↓                          │
│                                         │
│  OPENAI_API_KEY set?                    │
│       ├── Yes → return "openai"         │
│       └── No → raise ValueError         │
│                                         │
└─────────────────────────────────────────┘
```

---

## Part 9: URL Resolution Method

### get_llm_base_url()

```python
def get_llm_base_url(self) -> Optional[str]:
    """Get the base URL for the active LLM provider."""
    provider = self.get_active_llm_provider()
    if provider == "openrouter":
        return "https://openrouter.ai/api/v1"
    elif provider == "groq":
        return "https://api.groq.com/openai/v1"
    return None  # OpenAI uses default
```

### Provider URLs

| Provider | Base URL |
|----------|----------|
| OpenRouter | https://openrouter.ai/api/v1 |
| Groq | https://api.groq.com/openai/v1 |
| OpenAI | None (uses library default) |

---

## Part 10: API Key Resolution Method

### get_llm_api_key()

```python
def get_llm_api_key(self) -> str:
    """Get the API key for the active LLM provider."""
    provider = self.get_active_llm_provider()
    if provider == "openrouter":
        return self.openrouter_api_key
    elif provider == "groq":
        return self.groq_api_key
    return self.openai_api_key
```

This method pairs with `get_llm_base_url()` to provide both pieces of information needed to initialize an LLM client.

---

## Part 11: Singleton Pattern

### Global Settings Instance

```python
# Singleton instance
settings = Settings()
```

### Usage Pattern

```python
# In any module
from src.config import settings

# Access any setting
api_key = settings.openrouter_api_key
model = settings.llm_model
chunk_size = settings.chunk_size
```

### Why Singleton?

- **Consistency** — All modules share the same configuration
- **Performance** — Environment variables are loaded once
- **Simplicity** — No need to pass settings between functions

---

## Usage Examples

### Basic Access

```python
from src.config import settings

print(f"Using model: {settings.llm_model}")
print(f"Chunk size: {settings.chunk_size}")
```

### Provider-Aware LLM Initialization

```python
from src.config import settings
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model=settings.llm_model,
    openai_api_key=settings.get_llm_api_key(),
    openai_api_base=settings.get_llm_base_url(),
)
```

### Checking Configuration

```python
from src.config import settings

try:
    provider = settings.get_active_llm_provider()
    print(f"Active provider: {provider}")
except ValueError as e:
    print(f"Configuration error: {e}")
```

---

## Environment Variables Reference

| Variable | Type | Default | Required |
|----------|------|---------|----------|
| `OPENROUTER_API_KEY` | str | None | One of three |
| `GROQ_API_KEY` | str | None | One of three |
| `OPENAI_API_KEY` | str | None | One of three |
| `LANGFUSE_SECRET_KEY` | str | None | No |
| `LANGFUSE_PUBLIC_KEY` | str | None | No |
| `LANGFUSE_BASE_URL` | str | https://cloud.langfuse.com | No |
| `LLM_MODEL` | str | gpt-4o-mini | No |
| `EMBEDDING_MODEL` | str | text-embedding-3-small | No |
| `CHUNK_SIZE` | int | 800 | No |
| `CHUNK_OVERLAP` | int | 200 | No |
| `RETRIEVAL_K` | int | 4 | No |
| `DATA_DIR` | str | data | No |
| `VECTOR_STORE_PATH` | str | data/vectorstore | No |

---

*Document Version: 1.0*  
*Created: January 11, 2026*
