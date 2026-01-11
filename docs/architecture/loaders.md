# Document Loaders Module: Complete Guide

*Unified interface for loading various document types*

**File**: `src/loaders.py` | **Purpose**: PDF, DOCX, and TXT document ingestion

---

## Introduction

The `loaders.py` module provides a unified interface for loading documents of various formats into LangChain's `Document` objects. It abstracts away the complexity of different file formats, allowing the rest of the application to work with a consistent data structure regardless of the source document type.

---

## Part 1: Module Imports

### Dependencies

```python
from pathlib import Path
from typing import List, Union
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
```

| Import | Purpose |
|--------|---------|
| `Path` | Cross-platform file path handling |
| `List, Union` | Type hints for function signatures |
| `Document` | LangChain's standard document class |
| `PyPDFLoader` | Loads PDF files page by page |
| `Docx2txtLoader` | Loads Word documents |
| `TextLoader` | Loads plain text files |

---

## Part 2: Loader Selection Function

### get_loader()

```python
def get_loader(file_path: Union[str, Path]):
    """
    Get the appropriate loader based on file extension.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        Document loader instance
        
    Raises:
        ValueError: If file type is not supported
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()
    
    loaders = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt": TextLoader,
    }
    
    if extension not in loaders:
        supported = ", ".join(loaders.keys())
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported types: {supported}"
        )
    
    return loaders[extension](str(file_path))
```

### Loader Mapping

| Extension | Loader Class | Behavior |
|-----------|--------------|----------|
| `.pdf` | `PyPDFLoader` | One Document per page |
| `.docx` | `Docx2txtLoader` | Single Document with all text |
| `.txt` | `TextLoader` | Single Document with all text |

### Selection Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      get_loader(file_path)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: "document.pdf"                                          │
│           ↓                                                      │
│  Extract extension: ".pdf"                                       │
│           ↓                                                      │
│  Lookup in mapping: {".pdf": PyPDFLoader, ...}                  │
│           ↓                                                      │
│  Return: PyPDFLoader("document.pdf")                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 3: Single Document Loading

### load_document()

```python
def load_document(file_path: Union[str, Path]) -> List[Document]:
    """
    Load a document and return list of Document objects.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        List of Document objects with page_content and metadata
    """
    loader = get_loader(file_path)
    documents = loader.load()
    
    # Enrich metadata with source filename
    file_path = Path(file_path)
    for doc in documents:
        doc.metadata["source"] = file_path.name
        doc.metadata["file_path"] = str(file_path)
    
    return documents
```

### Document Structure

Each loaded document contains:

```python
Document(
    page_content="The actual text content...",
    metadata={
        "source": "report.pdf",        # Added by this function
        "file_path": "/path/to/report.pdf",  # Added by this function
        "page": 0,                     # From PyPDFLoader (PDFs only)
    }
)
```

### Loading Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   load_document("report.pdf")                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Get appropriate loader                                       │
│     └── PyPDFLoader("report.pdf")                               │
│              ↓                                                   │
│  2. Load documents                                               │
│     └── [Doc(page 0), Doc(page 1), Doc(page 2), ...]            │
│              ↓                                                   │
│  3. Enrich metadata for each document                           │
│     └── Add "source" and "file_path" fields                     │
│              ↓                                                   │
│  4. Return enriched document list                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 4: Batch Document Loading

### load_documents()

```python
def load_documents(file_paths: List[Union[str, Path]]) -> List[Document]:
    """
    Load multiple documents.
    
    Args:
        file_paths: List of paths to document files
        
    Returns:
        Combined list of Document objects from all files
    """
    all_documents = []
    for file_path in file_paths:
        try:
            docs = load_document(file_path)
            all_documents.extend(docs)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return all_documents
```

### Batch Processing

| Scenario | Behavior |
|----------|----------|
| All files load successfully | Returns combined document list |
| Some files fail | Logs error, continues with remaining files |
| All files fail | Returns empty list |

### Example Usage

```python
file_paths = [
    "documents/report.pdf",
    "documents/notes.txt",
    "documents/summary.docx",
]

all_docs = load_documents(file_paths)
print(f"Loaded {len(all_docs)} documents from {len(file_paths)} files")
```

---

## Part 5: Loader Characteristics

### PyPDFLoader Details

| Feature | Behavior |
|---------|----------|
| Output | One Document per page |
| Metadata | Includes `page` number |
| Text extraction | Basic PDF text extraction |
| Images | Not extracted (text only) |

### Docx2txtLoader Details

| Feature | Behavior |
|---------|----------|
| Output | Single Document with all content |
| Metadata | Basic file metadata |
| Formatting | Plain text (no styling) |
| Tables | Extracted as text |

### TextLoader Details

| Feature | Behavior |
|---------|----------|
| Output | Single Document |
| Encoding | UTF-8 by default |
| Line breaks | Preserved |

---

## Part 6: Error Handling

### Unsupported File Types

```python
try:
    docs = load_document("file.xlsx")
except ValueError as e:
    print(e)
    # "Unsupported file type: .xlsx. Supported types: .pdf, .docx, .txt"
```

### File Not Found

```python
try:
    docs = load_document("nonexistent.pdf")
except FileNotFoundError as e:
    print(e)
    # Raised by the underlying loader
```

### Corrupted Files

```python
try:
    docs = load_document("corrupted.pdf")
except Exception as e:
    print(f"Error: {e}")
    # Various exceptions depending on corruption type
```

---

## Usage Examples

### Basic Loading

```python
from src.loaders import load_document

docs = load_document("report.pdf")
for doc in docs:
    print(f"Page {doc.metadata.get('page', 'N/A')}: {doc.page_content[:100]}...")
```

### With Chunking

```python
from src.loaders import load_document
from src.chunker import chunk_documents

docs = load_document("large_document.pdf")
chunks = chunk_documents(docs)
print(f"Created {len(chunks)} chunks from {len(docs)} pages")
```

### Directory Processing

```python
from pathlib import Path
from src.loaders import load_documents

# Get all supported files from a directory
docs_dir = Path("documents")
files = list(docs_dir.glob("*.pdf")) + list(docs_dir.glob("*.txt"))

all_docs = load_documents(files)
```

---

## Integration with RAG Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG Pipeline                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User uploads files                                              │
│        ↓                                                         │
│  ┌──────────────────────────┐                                   │
│  │     loaders.py           │                                   │
│  │  load_document()         │ ◄── YOU ARE HERE                  │
│  └────────────┬─────────────┘                                   │
│               ↓                                                  │
│  ┌──────────────────────────┐                                   │
│  │     chunker.py           │                                   │
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
