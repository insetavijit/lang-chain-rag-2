# Embeddings Module: Complete Guide

*Vector generation for semantic similarity search*

**File**: `src/embeddings.py` | **Purpose**: Convert text to vector representations

---

## Introduction

The `embeddings.py` module handles the conversion of text into dense vector representations (embeddings). These vectors capture semantic meaning, enabling similarity search—the core mechanism behind RAG retrieval. This module provides a unified interface for embedding generation that works across different LLM providers.

---

## Part 1: Module Imports

### Dependencies

```python
from typing import List
from langchain_openai import OpenAIEmbeddings
from src.config import settings
```

| Import | Purpose |
|--------|---------|
| `List` | Type hints for vector lists |
| `OpenAIEmbeddings` | OpenAI embedding model wrapper |
| `settings` | Provider configuration |

---

## Part 2: Embedding Provider Factory

### get_embeddings()

```python
def get_embeddings() -> OpenAIEmbeddings:
    """
    Get configured embedding model instance.
    
    Returns:
        OpenAIEmbeddings instance configured for the active provider
    """
    provider = settings.get_active_llm_provider()
    
    if provider == "openrouter":
        return OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openrouter_api_key,
            openai_api_base="https://openrouter.ai/api/v1",
        )
    elif provider == "openai":
        return OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
        )
    else:
        # Fallback for Groq users
        if settings.openrouter_api_key:
            return OpenAIEmbeddings(
                model=settings.embedding_model,
                openai_api_key=settings.openrouter_api_key,
                openai_api_base="https://openrouter.ai/api/v1",
            )
        raise ValueError(
            "Embeddings require OpenRouter or OpenAI API key. "
            "Groq does not support embedding generation."
        )
```

### Provider Decision Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     get_embeddings() Logic                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Get active provider from config                                 │
│           ↓                                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Provider = "openrouter"?                                 │    │
│  │    └─→ Use OpenRouter with OpenAI-compatible endpoint   │    │
│  │                                                          │    │
│  │ Provider = "openai"?                                     │    │
│  │    └─→ Use OpenAI directly                              │    │
│  │                                                          │    │
│  │ Provider = "groq"?                                       │    │
│  │    └─→ Check for OpenRouter fallback                    │    │
│  │        ├─→ Found: Use OpenRouter                        │    │
│  │        └─→ Not found: Raise ValueError                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Provider Support

| Provider | Embeddings Support | Notes |
|----------|-------------------|-------|
| OpenRouter | ✅ Yes | Via OpenAI-compatible API |
| OpenAI | ✅ Yes | Native support |
| Groq | ❌ No | Falls back to OpenRouter |

> [!IMPORTANT]
> Groq does not offer embedding models. If using Groq for LLM, you must also have an OpenRouter or OpenAI key for embeddings.

---

## Part 3: Batch Embedding Function

### embed_texts()

```python
def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts.
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        List of embedding vectors (each is a list of floats)
    """
    embeddings = get_embeddings()
    return embeddings.embed_documents(texts)
```

### Batch Processing

```
Input: ["Hello world", "How are you?", "RAG systems"]
            ↓
    Embed in batch (efficient API call)
            ↓
Output: [
    [0.0234, -0.0156, 0.0412, ...],  # 1536 dimensions
    [0.0178, -0.0089, 0.0523, ...],  # 1536 dimensions
    [0.0312, -0.0234, 0.0189, ...],  # 1536 dimensions
]
```

### When to Use

- **Document indexing** — Embed all chunks before storing in vector database
- **Batch processing** — More efficient than individual calls

---

## Part 4: Query Embedding Function

### embed_query()

```python
def embed_query(text: str) -> List[float]:
    """
    Generate embedding for a single query text.
    
    Args:
        text: Query text to embed
        
    Returns:
        Embedding vector as list of floats
    """
    embeddings = get_embeddings()
    return embeddings.embed_query(text)
```

### Query vs Document Embedding

| Method | Use Case | API Call |
|--------|----------|----------|
| `embed_documents()` | Indexing multiple chunks | Batch |
| `embed_query()` | Single user question | Single |

> [!NOTE]
> Some embedding models optimize differently for queries vs documents. Using the correct method ensures optimal retrieval performance.

---

## Part 5: Embedding Model Details

### text-embedding-3-small

| Property | Value |
|----------|-------|
| Dimensions | 1536 |
| Max tokens | 8191 |
| Cost | ~$0.02 per 1M tokens |
| Performance | Good for most use cases |

### Vector Representation

```
Text: "Machine learning is a subset of artificial intelligence"

Embedding (1536 dimensions):
[
    0.0234,    # dimension 0
   -0.0156,    # dimension 1
    0.0412,    # dimension 2
    ...
    0.0089,    # dimension 1533
   -0.0312,    # dimension 1534
    0.0178     # dimension 1535
]
```

---

## Part 6: How Embeddings Enable RAG

### Semantic Similarity

```
┌─────────────────────────────────────────────────────────────────┐
│                    Embedding Similarity Search                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Query: "How does photosynthesis work?"                         │
│                           ↓                                      │
│  Query Embedding: [0.0234, -0.0156, 0.0412, ...]               │
│                           ↓                                      │
│  Compare with stored document embeddings:                        │
│                                                                  │
│  Doc 1: "Plants convert sunlight to energy"                     │
│         [0.0228, -0.0148, 0.0398, ...]                         │
│         Similarity: 0.92 ✓ HIGH MATCH                          │
│                                                                  │
│  Doc 2: "The stock market closed higher"                        │
│         [0.0567, 0.0234, -0.0189, ...]                         │
│         Similarity: 0.15 ✗ LOW MATCH                           │
│                                                                  │
│  Doc 3: "Chlorophyll absorbs light energy"                      │
│         [0.0219, -0.0162, 0.0405, ...]                         │
│         Similarity: 0.89 ✓ HIGH MATCH                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Usage Examples

### Basic Embedding

```python
from src.embeddings import embed_query, embed_texts

# Single query
vector = embed_query("What is machine learning?")
print(f"Vector dimensions: {len(vector)}")  # 1536

# Multiple documents
texts = ["Document 1 content", "Document 2 content"]
vectors = embed_texts(texts)
print(f"Generated {len(vectors)} embeddings")
```

### Custom Provider Check

```python
from src.embeddings import get_embeddings

embeddings = get_embeddings()
print(f"Model: {embeddings.model}")
```

### With Vector Store

```python
from src.embeddings import get_embeddings
from langchain_community.vectorstores import FAISS

embeddings = get_embeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
```

---

## Integration with RAG Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG Pipeline                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────┐                                   │
│  │     chunker.py           │                                   │
│  │  chunk_documents()       │                                   │
│  └────────────┬─────────────┘                                   │
│               ↓                                                  │
│  ┌──────────────────────────┐                                   │
│  │    embeddings.py         │ ◄── YOU ARE HERE                  │
│  │  get_embeddings()        │     (Used internally by           │
│  │  embed_texts()           │      vectorstore.py)              │
│  └────────────┬─────────────┘                                   │
│               ↓                                                  │
│  ┌──────────────────────────┐                                   │
│  │   vectorstore.py         │                                   │
│  │  create_vectorstore()    │                                   │
│  └──────────────────────────┘                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Document Version: 1.0*  
*Created: January 11, 2026*
