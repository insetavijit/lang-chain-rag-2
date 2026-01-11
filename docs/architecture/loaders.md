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

## Part 5: Under the Hood - Detailed Function Breakdown

This section explains **exactly what happens** when each function is called, step by step.

---

### 🔍 get_loader() - Deep Dive

**Purpose**: Factory function that returns the correct loader instance based on file extension.

```python
def get_loader(file_path: Union[str, Path]):
```

#### Step-by-Step Execution:

| Step | Code | What Happens |
|------|------|--------------|
| 1 | `file_path = Path(file_path)` | Converts string to `Path` object for cross-platform compatibility |
| 2 | `extension = file_path.suffix.lower()` | Extracts extension (e.g., `.pdf`) and lowercases it |
| 3 | `loaders = {...}` | Creates mapping dictionary of extension → loader class |
| 4 | `if extension not in loaders` | Checks if file type is supported |
| 5 | `return loaders[extension](str(file_path))` | **Instantiates** the loader class with file path |

#### What Each Loader Does Internally:

| Loader | Library Used | Internal Process |
|--------|--------------|------------------|
| `PyPDFLoader` | `pypdf` | Opens PDF binary → Parses each page → Extracts text per page |
| `Docx2txtLoader` | `docx2txt` | Unzips `.docx` (it's a ZIP!) → Parses `document.xml` → Extracts text |
| `TextLoader` | Python built-in | Opens file with `open()` → Reads with UTF-8 encoding |

#### Memory Diagram:

```
Input: "report.pdf"
         ↓
┌─────────────────────────────────────────────────────┐
│  Step 1: Path("report.pdf")                          │
│  Result: PosixPath('report.pdf') or WindowsPath(...) │
├─────────────────────────────────────────────────────┤
│  Step 2: path.suffix.lower()                         │
│  Result: ".pdf"                                      │
├─────────────────────────────────────────────────────┤
│  Step 3: loaders[".pdf"]                             │
│  Result: <class 'PyPDFLoader'>  (not instance yet!)  │
├─────────────────────────────────────────────────────┤
│  Step 4: PyPDFLoader("report.pdf")                   │
│  Result: <PyPDFLoader instance>  ← READY TO LOAD     │
└─────────────────────────────────────────────────────┘
```

---

### 🔍 load_document() - Deep Dive

**Purpose**: Loads a single file and returns LangChain Document objects with enriched metadata.

```python
def load_document(file_path: Union[str, Path]) -> List[Document]:
```

#### Step-by-Step Execution:

| Step | Code | What Happens | Data State |
|------|------|--------------|------------|
| 1 | `loader = get_loader(file_path)` | Gets configured loader instance | `loader = PyPDFLoader(...)` |
| 2 | `documents = loader.load()` | **Reads file from disk, parses content** | `[Doc1, Doc2, ...]` |
| 3 | `file_path = Path(file_path)` | Converts to Path for metadata extraction | `Path('report.pdf')` |
| 4 | `for doc in documents:` | Iterates through each document | Processing each |
| 5 | `doc.metadata["source"] = file_path.name` | Adds filename to metadata | `"report.pdf"` |
| 6 | `doc.metadata["file_path"] = str(file_path)` | Adds full path to metadata | `"/full/path/report.pdf"` |
| 7 | `return documents` | Returns enriched document list | Final output |

#### What `.load()` Does for Each Loader:

**PyPDFLoader.load():**
```
┌──────────────────────────────────────────────────────────────────┐
│  1. Open PDF file in binary mode: open("file.pdf", "rb")         │
│  2. Create PdfReader object from pypdf library                    │
│  3. Iterate through reader.pages:                                 │
│     └── For each page:                                            │
│         ├── page.extract_text() → raw text string                │
│         ├── Create Document(page_content=text)                   │
│         └── Add metadata: {"page": 0, "source": "file.pdf"}      │
│  4. Return list of Documents (one per page)                      │
└──────────────────────────────────────────────────────────────────┘
```

**Docx2txtLoader.load():**
```
┌──────────────────────────────────────────────────────────────────┐
│  1. DOCX is actually a ZIP file containing XML!                   │
│  2. Extract and parse word/document.xml                           │
│  3. Walk through XML nodes, extracting text from <w:t> tags      │
│  4. Also extracts text from headers, footers, text boxes         │
│  5. Return SINGLE Document with all text concatenated            │
└──────────────────────────────────────────────────────────────────┘
```

**TextLoader.load():**
```
┌──────────────────────────────────────────────────────────────────┐
│  1. Open file: open("file.txt", encoding="utf-8")                │
│  2. Read entire content: content = file.read()                   │
│  3. Create single Document(page_content=content)                 │
│  4. Add basic metadata: {"source": "file.txt"}                   │
│  5. Return list with single Document                             │
└──────────────────────────────────────────────────────────────────┘
```

#### Document Object Structure:

```python
# Before metadata enrichment (from loader):
Document(
    page_content="The quick brown fox...",
    metadata={"page": 0}  # Only for PDFs
)

# After metadata enrichment (from load_document):
Document(
    page_content="The quick brown fox...",
    metadata={
        "page": 0,                        # From PyPDFLoader
        "source": "report.pdf",           # Added by load_document()
        "file_path": "C:/docs/report.pdf" # Added by load_document()
    }
)
```

#### Why Enrich Metadata?

| Metadata Field | Purpose | Used By |
|----------------|---------|---------|
| `source` | Display filename in UI | Streamlit app |
| `file_path` | Full path for debugging | Error messages |
| `page` | Track which page content came from | Citation in answers |

---

### 🔍 load_documents() - Deep Dive

**Purpose**: Batch load multiple files with error tolerance.

```python
def load_documents(file_paths: List[Union[str, Path]]) -> List[Document]:
```

#### Step-by-Step Execution:

| Step | Code | What Happens |
|------|------|--------------|
| 1 | `all_documents = []` | Initialize empty list for accumulating results |
| 2 | `for file_path in file_paths:` | Iterate through each input path |
| 3 | `try:` | Begin error handling block |
| 4 | `docs = load_document(file_path)` | Load single document (calls function above) |
| 5 | `all_documents.extend(docs)` | **Append** all docs from this file to main list |
| 6 | `except Exception as e:` | Catch ANY error (file not found, corrupted, etc.) |
| 7 | `print(f"Error loading...")` | Log error but **don't stop** processing |
| 8 | `return all_documents` | Return whatever was successfully loaded |

#### Why `extend()` Instead of `append()`?

```python
# WRONG - append() would create nested list:
all_documents.append([doc1, doc2])
# Result: [[doc1, doc2], [doc3, doc4]]  ← Nested!

# CORRECT - extend() flattens into single list:
all_documents.extend([doc1, doc2])
# Result: [doc1, doc2, doc3, doc4]  ← Flat!
```

#### Error Handling Strategy:

```
Input: ["valid.pdf", "corrupted.pdf", "notes.txt"]
          ↓
┌────────────────────────────────────────────────────────────┐
│  File 1: valid.pdf     → ✅ Load success → Add 5 docs     │
│  File 2: corrupted.pdf → ❌ Exception → Print error, skip │
│  File 3: notes.txt     → ✅ Load success → Add 1 doc      │
├────────────────────────────────────────────────────────────┤
│  Output: [6 documents total]                                │
│  Console: "Error loading corrupted.pdf: ..."               │
└────────────────────────────────────────────────────────────┘
```

This **fault-tolerant design** ensures:
- One bad file doesn't crash the entire upload
- User gets partial results instead of nothing
- Errors are logged for debugging

---

## Part 6: Loader Characteristics

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
