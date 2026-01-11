# Chunker Module: Complete Guide

*Text splitting strategies for optimal retrieval*

**File**: `src/chunker.py` | **Purpose**: Split documents into retrievable chunks

---

## Introduction

The `chunker.py` module handles the critical task of splitting documents into smaller chunks suitable for embedding and retrieval. Proper chunking directly impacts RAG quality—chunks that are too large dilute relevance, while chunks that are too small lose context. This module uses LangChain's `RecursiveCharacterTextSplitter` to intelligently split text at natural boundaries.

---

## Part 1: Module Imports

### Dependencies

```python
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import settings
```

| Import | Purpose |
|--------|---------|
| `List` | Type hint for return values |
| `Document` | LangChain's document container |
| `RecursiveCharacterTextSplitter` | Intelligent text splitting |
| `settings` | Configuration defaults |

---

## Part 2: Text Splitter Factory

### create_text_splitter()

```python
def create_text_splitter(
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> RecursiveCharacterTextSplitter:
    """
    Create a text splitter with configured parameters.
    
    Args:
        chunk_size: Maximum size of each chunk (uses config default if None)
        chunk_overlap: Overlap between chunks (uses config default if None)
        
    Returns:
        Configured RecursiveCharacterTextSplitter instance
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size or settings.chunk_size,
        chunk_overlap=chunk_overlap or settings.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
        is_separator_regex=False,
    )
```

### Configuration Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `chunk_size` | 800 | Maximum characters per chunk |
| `chunk_overlap` | 200 | Characters shared between adjacent chunks |
| `length_function` | `len` | How to measure chunk length |
| `separators` | ["\n\n", "\n", ". ", " ", ""] | Split priority order |

### Separator Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│              RecursiveCharacterTextSplitter Logic                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Try separators in order until chunk fits within size limit:    │
│                                                                  │
│  1. "\n\n" → Split on paragraph breaks (preferred)              │
│        ↓                                                         │
│  2. "\n"   → Split on line breaks                               │
│        ↓                                                         │
│  3. ". "   → Split on sentences                                 │
│        ↓                                                         │
│  4. " "    → Split on words                                     │
│        ↓                                                         │
│  5. ""     → Split on characters (last resort)                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 3: Document Chunking

### chunk_documents()

```python
def chunk_documents(
    documents: List[Document],
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> List[Document]:
    """
    Split documents into chunks.
    
    Args:
        documents: List of Document objects to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of chunked Document objects with preserved metadata
    """
    text_splitter = create_text_splitter(chunk_size, chunk_overlap)
    chunks = text_splitter.split_documents(documents)
    
    # Add chunk index to metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
    
    return chunks
```

### Chunking Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    Document Chunking Process                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: [Document(2500 chars), Document(1800 chars)]            │
│                         ↓                                        │
│  Split using RecursiveCharacterTextSplitter (800 char chunks)   │
│                         ↓                                        │
│  Output: [                                                       │
│    Document(chunk 0, ~800 chars, metadata={chunk_index: 0}),    │
│    Document(chunk 1, ~800 chars, metadata={chunk_index: 1}),    │
│    Document(chunk 2, ~800 chars, metadata={chunk_index: 2}),    │
│    Document(chunk 3, ~800 chars, metadata={chunk_index: 3}),    │
│    Document(chunk 4, ~500 chars, metadata={chunk_index: 4}),    │
│  ]                                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Metadata Preservation

The splitter preserves original metadata and adds `chunk_index`:

```python
# Original document
Document(
    page_content="Long text...",
    metadata={"source": "report.pdf", "page": 3}
)

# After chunking
Document(
    page_content="Chunk of text...",
    metadata={"source": "report.pdf", "page": 3, "chunk_index": 0}
)
```

---

## Part 4: Raw Text Chunking

### chunk_text()

```python
def chunk_text(
    text: str,
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> List[str]:
    """
    Split raw text into chunks.
    
    Args:
        text: Raw text string to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    text_splitter = create_text_splitter(chunk_size, chunk_overlap)
    return text_splitter.split_text(text)
```

### Use Case

Use `chunk_text()` when you have raw strings instead of Document objects:

```python
raw_text = "Your long text content here..."
chunks = chunk_text(raw_text)
# Returns: ["chunk 1...", "chunk 2...", "chunk 3..."]
```

---

## Part 5: Overlap Explained

### Why Overlap?

```
Without overlap (chunk_overlap=0):

┌────────────────────┐┌────────────────────┐
│      Chunk 1       ││      Chunk 2       │
│ "...important      ││  concept that..."  │
│  concept"          ││                    │
└────────────────────┘└────────────────────┘
           ↑                    ↑
     Information split across chunks!
     Query for "important concept" may miss context.

With overlap (chunk_overlap=200):

┌────────────────────┐
│      Chunk 1       │
│ "...important      │
│  concept that      │
│  explains..."      │
└───────────┬────────┘
            │ 200 char overlap
┌───────────┴────────┐
│      Chunk 2       │
│  concept that      │
│  explains the      │
│  theory of..."     │
└────────────────────┘
     ↑
  Context preserved across boundaries!
```

### Overlap Trade-offs

| Overlap | Pros | Cons |
|---------|------|------|
| Small (50-100) | Less duplication, faster indexing | May lose context |
| Medium (200) | Good balance | Recommended default |
| Large (300+) | Maximum context | More storage, redundancy |

---

## Part 6: Chunk Size Strategy

### Size Recommendations

| Use Case | Chunk Size | Rationale |
|----------|------------|-----------|
| Technical docs | 600-800 | Dense information, need precision |
| Narratives | 1000-1200 | Need more context for flow |
| Legal/Contracts | 400-600 | Precise clause matching |
| Q&A/FAQ | 300-500 | Short, specific answers |

### Trade-offs

```
┌─────────────────────────────────────────────────────────────────┐
│                     Chunk Size Trade-offs                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Smaller chunks (300-500):                                       │
│  ✓ More precise retrieval                                       │
│  ✓ Less noise in context                                        │
│  ✗ May lack sufficient context                                  │
│  ✗ More chunks to process                                       │
│                                                                  │
│  Larger chunks (1000-1500):                                      │
│  ✓ More context per retrieval                                   │
│  ✓ Fewer chunks overall                                         │
│  ✗ May include irrelevant content                               │
│  ✗ Less precise matching                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Usage Examples

### Basic Chunking

```python
from src.loaders import load_document
from src.chunker import chunk_documents

# Load and chunk
docs = load_document("large_report.pdf")
chunks = chunk_documents(docs)

print(f"Original: {len(docs)} pages")
print(f"Chunked: {len(chunks)} chunks")
```

### Custom Parameters

```python
# Smaller chunks for precise retrieval
chunks = chunk_documents(docs, chunk_size=400, chunk_overlap=100)

# Larger chunks for more context
chunks = chunk_documents(docs, chunk_size=1200, chunk_overlap=300)
```

### Direct Text Chunking

```python
from src.chunker import chunk_text

text = open("article.txt").read()
text_chunks = chunk_text(text)

for i, chunk in enumerate(text_chunks):
    print(f"Chunk {i}: {len(chunk)} characters")
```

---

## Integration with RAG Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG Pipeline                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────┐                                   │
│  │     loaders.py           │                                   │
│  │  load_document()         │                                   │
│  └────────────┬─────────────┘                                   │
│               ↓                                                  │
│  ┌──────────────────────────┐                                   │
│  │     chunker.py           │ ◄── YOU ARE HERE                  │
│  │  chunk_documents()       │                                   │
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
