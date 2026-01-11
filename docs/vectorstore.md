# Vector Store Module: Complete Guide

*FAISS vector database operations for similarity search*

**File**: `src/vectorstore.py` | **Purpose**: Create, persist, and query vector indices

---

## Introduction

The `vectorstore.py` module manages all interactions with the FAISS vector database—the engine that powers similarity search in the RAG system. FAISS (Facebook AI Similarity Search) is an efficient library for searching in high-dimensional vector spaces, perfect for finding relevant document chunks based on semantic similarity.

---

## Part 1: Module Imports

### Dependencies

```python
from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from src.embeddings import get_embeddings
from src.config import settings
```

| Import | Purpose |
|--------|---------|
| `Path` | File system path handling |
| `List, Optional` | Type hints |
| `Document` | LangChain document container |
| `FAISS` | Vector store implementation |
| `get_embeddings` | Embedding model provider |
| `settings` | Configuration (paths, retrieval_k) |

---

## Part 2: Vector Store Creation

### create_vectorstore()

```python
def create_vectorstore(documents: List[Document]) -> FAISS:
    """
    Create a new FAISS vector store from documents.
    
    Args:
        documents: List of Document objects to index
        
    Returns:
        FAISS vector store instance
    """
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore
```

### Creation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    create_vectorstore() Flow                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: [Document, Document, Document, ...]                     │
│                         ↓                                        │
│  1. Get embedding model from embeddings.py                      │
│                         ↓                                        │
│  2. Extract text from each document                             │
│                         ↓                                        │
│  3. Generate embeddings for all texts (batch API call)          │
│                         ↓                                        │
│  4. Create FAISS index with vectors                             │
│                         ↓                                        │
│  5. Store document references for retrieval                     │
│                         ↓                                        │
│  Output: FAISS vectorstore object                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 3: Persistence Operations

### save_vectorstore()

```python
def save_vectorstore(vectorstore: FAISS, path: Optional[str] = None) -> None:
    """
    Save vector store to disk.
    
    Args:
        vectorstore: FAISS vector store to save
        path: Directory path for saving (uses config default if None)
    """
    save_path = Path(path or settings.vector_store_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(save_path))
```

### load_vectorstore()

```python
def load_vectorstore(path: Optional[str] = None) -> FAISS:
    """
    Load vector store from disk.
    
    Args:
        path: Directory path to load from (uses config default if None)
        
    Returns:
        FAISS vector store instance
        
    Raises:
        FileNotFoundError: If vector store doesn't exist at path
    """
    load_path = Path(path or settings.vector_store_path)
    if not load_path.exists():
        raise FileNotFoundError(f"Vector store not found at {load_path}")
    
    embeddings = get_embeddings()
    return FAISS.load_local(
        str(load_path), 
        embeddings,
        allow_dangerous_deserialization=True
    )
```

### File Structure

```
data/vectorstore/
├── index.faiss    # Binary vector index
└── index.pkl      # Document metadata (pickled)
```

> [!IMPORTANT]
> `allow_dangerous_deserialization=True` is required when loading FAISS indices that were saved with pickle. Only load indices you trust.

---

## Part 4: Existence Check

### vectorstore_exists()

```python
def vectorstore_exists(path: Optional[str] = None) -> bool:
    """
    Check if a vector store exists at the given path.
    
    Args:
        path: Directory path to check (uses config default if None)
        
    Returns:
        True if vector store exists, False otherwise
    """
    load_path = Path(path or settings.vector_store_path)
    return load_path.exists() and (load_path / "index.faiss").exists()
```

### Why Check Both?

| Condition | Meaning |
|-----------|---------|
| Directory exists | Path is valid |
| `index.faiss` exists | Complete FAISS index present |

Checking both prevents false positives from empty directories.

---

## Part 5: Adding Documents

### add_documents()

```python
def add_documents(
    vectorstore: FAISS, 
    documents: List[Document]
) -> FAISS:
    """
    Add new documents to existing vector store.
    
    Args:
        vectorstore: Existing FAISS vector store
        documents: New documents to add
        
    Returns:
        Updated vector store
    """
    vectorstore.add_documents(documents)
    return vectorstore
```

### Incremental Updates

```
┌──────────────────────────────────────┐
│     Existing Vector Store            │
│  [Doc A, Doc B, Doc C] → 3 vectors   │
└───────────────┬──────────────────────┘
                ↓
        add_documents([Doc D, Doc E])
                ↓
┌──────────────────────────────────────┐
│     Updated Vector Store             │
│  [A, B, C, D, E] → 5 vectors         │
└──────────────────────────────────────┘
```

---

## Part 6: Similarity Search

### similarity_search()

```python
def similarity_search(
    vectorstore: FAISS,
    query: str,
    k: Optional[int] = None,
) -> List[Document]:
    """
    Search for similar documents.
    
    Args:
        vectorstore: FAISS vector store to search
        query: Query text
        k: Number of results to return (uses config default if None)
        
    Returns:
        List of most similar Document objects
    """
    return vectorstore.similarity_search(
        query, 
        k=k or settings.retrieval_k
    )
```

### How Search Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     Similarity Search Process                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Query: "What is machine learning?"                             │
│                         ↓                                        │
│  1. Embed query → [0.023, -0.015, 0.041, ...]                  │
│                         ↓                                        │
│  2. Compare with all vectors in FAISS index                     │
│                         ↓                                        │
│  3. Compute cosine similarity scores                            │
│     - Doc 1: 0.89                                               │
│     - Doc 2: 0.45                                               │
│     - Doc 3: 0.92                                               │
│     - Doc 4: 0.67                                               │
│                         ↓                                        │
│  4. Return top-k documents (k=4 default)                        │
│     [Doc 3 (0.92), Doc 1 (0.89), Doc 4 (0.67), Doc 2 (0.45)]   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 7: Search with Scores

### similarity_search_with_score()

```python
def similarity_search_with_score(
    vectorstore: FAISS,
    query: str,
    k: Optional[int] = None,
) -> List[tuple[Document, float]]:
    """
    Search for similar documents with relevance scores.
    
    Args:
        vectorstore: FAISS vector store to search
        query: Query text
        k: Number of results to return (uses config default if None)
        
    Returns:
        List of (Document, score) tuples
    """
    return vectorstore.similarity_search_with_score(
        query,
        k=k or settings.retrieval_k
    )
```

### Score Interpretation

| Score Range | Meaning |
|-------------|---------|
| 0.0 - 0.3 | Low similarity (distant) |
| 0.3 - 0.6 | Moderate similarity |
| 0.6 - 0.8 | Good similarity |
| 0.8 - 1.0 | High similarity (very relevant) |

> [!NOTE]
> FAISS returns L2 distance by default. Lower scores = more similar. LangChain may normalize this depending on configuration.

---

## Part 8: FAISS Internals

### Index Types

| Index | Use Case | Speed | Accuracy |
|-------|----------|-------|----------|
| Flat | Small datasets | Fast | Exact |
| IVF | Medium datasets | Faster | Approximate |
| HNSW | Large datasets | Fastest | Approximate |

LangChain uses `IndexFlatL2` by default—exact search suitable for most RAG applications.

### Memory Usage

```
Approximate memory per vector:
- 1536 dimensions × 4 bytes (float32) = 6,144 bytes ≈ 6 KB

For 10,000 documents:
- 10,000 × 6 KB = 60 MB

For 100,000 documents:
- 100,000 × 6 KB = 600 MB
```

---

## Usage Examples

### Basic Workflow

```python
from src.loaders import load_document
from src.chunker import chunk_documents
from src.vectorstore import (
    create_vectorstore,
    save_vectorstore,
    similarity_search
)

# Create and persist
docs = load_document("report.pdf")
chunks = chunk_documents(docs)
vectorstore = create_vectorstore(chunks)
save_vectorstore(vectorstore)

# Search
results = similarity_search(vectorstore, "What is the conclusion?")
for doc in results:
    print(doc.page_content[:200])
```

### Loading Existing Store

```python
from src.vectorstore import load_vectorstore, vectorstore_exists

if vectorstore_exists():
    vectorstore = load_vectorstore()
    print("Loaded existing vector store")
else:
    print("No vector store found")
```

### Search with Scores

```python
from src.vectorstore import similarity_search_with_score

results = similarity_search_with_score(vectorstore, "machine learning")
for doc, score in results:
    print(f"Score: {score:.3f} | {doc.page_content[:100]}")
```

---

## Integration with RAG Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG Pipeline                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────┐                                   │
│  │    embeddings.py         │                                   │
│  │  get_embeddings()        │                                   │
│  └────────────┬─────────────┘                                   │
│               ↓                                                  │
│  ┌──────────────────────────┐                                   │
│  │   vectorstore.py         │ ◄── YOU ARE HERE                  │
│  │  create_vectorstore()    │                                   │
│  │  similarity_search()     │                                   │
│  └────────────┬─────────────┘                                   │
│               ↓                                                  │
│  ┌──────────────────────────┐                                   │
│  │      chain.py            │                                   │
│  │  query_rag()            │                                   │
│  └──────────────────────────┘                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Document Version: 1.0*  
*Created: January 11, 2026*
