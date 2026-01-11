# RAG Document Q&A System: Application Guide

*A comprehensive breakdown of the Streamlit application architecture*

**File**: `app.py` | **Purpose**: Main entry point for the web interface

---

## Introduction

The `app.py` file serves as the central hub of the RAG Document Q&A System—the user-facing application that brings together document processing, vector search, and LLM-powered question answering into an intuitive chat interface. Built with Streamlit, it provides a responsive web application that users can access through their browser.

This document walks through each section of `app.py`, explaining the purpose, design decisions, and implementation details of every code block. Understanding this file is essential for customizing the application or extending its functionality.

---

## Part 1: Module Header & Imports

### Docstring & Core Imports

```python
"""
RAG Document Q&A System - Streamlit Application

Main entry point for the Streamlit web interface.
Run with: streamlit run app.py
"""

import streamlit as st
from pathlib import Path
import tempfile
import os
```

| Import | Purpose |
|--------|---------|
| `streamlit` | Core framework for building the web UI |
| `pathlib.Path` | Cross-platform file path handling |
| `tempfile` | Creating temporary files for uploaded documents |
| `os` | File system operations (cleanup) |

### Why These Imports?

- **streamlit as st** — The convention is to import Streamlit as `st` for brevity. Every UI element (buttons, text inputs, layouts) comes from this module.
- **Path** — Used to extract file extensions from uploaded files reliably across operating systems.
- **tempfile** — Uploaded files in Streamlit exist only in memory. We need to write them to temporary files so document loaders can process them.
- **os** — After processing, temporary files are deleted using `os.unlink()` to prevent disk clutter.

---

## Part 2: Page Configuration

### Streamlit Page Setup

```python
# Page configuration
st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)
```

| Parameter | Value | Effect |
|-----------|-------|--------|
| `page_title` | "RAG Document Q&A" | Browser tab title |
| `page_icon` | 📚 | Favicon shown in browser |
| `layout` | "wide" | Uses full browser width |
| `initial_sidebar_state` | "expanded" | Sidebar open by default |

### Critical Placement Note

> [!IMPORTANT]
> `st.set_page_config()` **must be the first Streamlit command** in your script. Any Streamlit calls before it will cause an error. This is why project imports come after this configuration block.

---

## Part 3: Project Module Imports

### Importing Core Components

```python
# Import after st.set_page_config to avoid issues
from src.config import settings
from src.loaders import load_document
from src.chunker import chunk_documents
from src.vectorstore import (
    create_vectorstore,
    save_vectorstore,
    load_vectorstore,
    vectorstore_exists,
)
from src.chain import query_rag, get_llm
from src.memory import get_session_memory, clear_session_memory
```

### Component Responsibility Map

| Module | Functions | Purpose |
|--------|-----------|---------|
| `src.config` | `settings` | Application configuration (API keys, model settings) |
| `src.loaders` | `load_document` | Parse PDF, DOCX, TXT files into Documents |
| `src.chunker` | `chunk_documents` | Split documents into retrievable chunks |
| `src.vectorstore` | `create_vectorstore`, `save_vectorstore`, `load_vectorstore`, `vectorstore_exists` | FAISS vector database operations |
| `src.chain` | `query_rag`, `get_llm` | RAG chain execution and LLM access |
| `src.memory` | `get_session_memory`, `clear_session_memory` | Conversation history management |

### Architecture Flow

```
User Upload → load_document → chunk_documents → create_vectorstore
                                                       ↓
                                              save_vectorstore
                                                       ↓
User Query → query_rag (retrieves from vectorstore) → LLM Response
```

---

## Part 4: Session State Initialization

### Managing Application State

```python
# Initialize session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = []
if "messages" not in st.session_state:
    st.session_state.messages = []
```

### Understanding Session State

Streamlit reruns the entire script on every user interaction. Without `st.session_state`, all variables would reset. Session state provides persistent storage across reruns.

| State Variable | Type | Purpose |
|----------------|------|---------|
| `vectorstore` | FAISS object or None | The loaded vector index for similarity search |
| `documents_loaded` | List[str] | Names of processed documents (for UI display) |
| `messages` | List[dict] | Chat history with role, content, and sources |

### State Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│                    Session State                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  First Visit:                                           │
│  vectorstore = None                                     │
│  documents_loaded = []                                  │
│  messages = []                                          │
│                                                         │
│  After Upload:                                          │
│  vectorstore = <FAISS object>                           │
│  documents_loaded = ["report.pdf", "notes.txt"]         │
│  messages = []                                          │
│                                                         │
│  After Chat:                                            │
│  messages = [                                           │
│    {"role": "user", "content": "..."},                  │
│    {"role": "assistant", "content": "...", sources:[]}  │
│  ]                                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Part 5: Vector Store Initialization Function

### Loading Persisted Data

```python
def init_vectorstore():
    """Load existing vectorstore if available."""
    if vectorstore_exists():
        try:
            st.session_state.vectorstore = load_vectorstore()
            return True
        except Exception as e:
            st.error(f"Failed to load vector store: {e}")
    return False
```

### Function Behavior

| Scenario | Action | Return |
|----------|--------|--------|
| Vector store exists on disk | Load into session state | `True` |
| Loading fails | Display error message | `False` |
| No vector store exists | Do nothing | `False` |

### Why Check Existence First?

The `vectorstore_exists()` check prevents unnecessary error handling for first-time users who haven't uploaded any documents yet. It creates a smoother user experience by distinguishing between "no data" and "corrupted data" scenarios.

---

## Part 6: Sidebar - Document Upload Section

### Upload Interface

```python
# Sidebar
with st.sidebar:
    st.title("📚 RAG Document Q&A")
    st.markdown("---")
    
    # Document Upload Section
    st.header("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Upload PDF, DOCX, or TXT files",
    )
```

### File Uploader Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `type` | ["pdf", "docx", "txt"] | Restricts accepted file types |
| `accept_multiple_files` | True | Allows batch uploads |
| `help` | "Upload PDF..." | Tooltip on hover |

### Sidebar Layout

```
┌─────────────────────────┐
│ 📚 RAG Document Q&A     │
├─────────────────────────┤
│ 📄 Upload Documents     │
│ ┌─────────────────────┐ │
│ │ File Uploader       │ │
│ └─────────────────────┘ │
│ [🔄 Process Documents]  │
├─────────────────────────┤
│ 📁 Loaded Documents     │
│ • report.pdf            │
│ • notes.txt             │
├─────────────────────────┤
│ ⚙️ Settings             │
│ Provider: OPENROUTER    │
│ Model: gpt-4o-mini      │
│ [🗑️ Clear Chat]         │
└─────────────────────────┘
```

---

## Part 7: Document Processing Pipeline

### Processing Uploaded Files

```python
if uploaded_files:
    if st.button("🔄 Process Documents", type="primary"):
        with st.spinner("Processing documents..."):
            all_documents = []
            
            for uploaded_file in uploaded_files:
                # Save to temp file
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=Path(uploaded_file.name).suffix
                ) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                try:
                    # Load and process
                    docs = load_document(tmp_path)
                    all_documents.extend(docs)
                    st.session_state.documents_loaded.append(uploaded_file.name)
                except Exception as e:
                    st.error(f"Error loading {uploaded_file.name}: {e}")
                finally:
                    os.unlink(tmp_path)
```

### Processing Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                    Document Processing Pipeline                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. User clicks "Process Documents"                               │
│            ↓                                                      │
│  2. FOR EACH uploaded file:                                       │
│     ├─→ Write to temporary file (with correct extension)         │
│     ├─→ Load document using appropriate loader                   │
│     ├─→ Add pages to all_documents list                          │
│     ├─→ Track filename in session state                          │
│     └─→ Delete temporary file (cleanup)                          │
│            ↓                                                      │
│  3. Chunk all documents                                           │
│            ↓                                                      │
│  4. Create vector store from chunks                               │
│            ↓                                                      │
│  5. Save vector store to disk                                     │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Temporary files | Document loaders require file paths, not memory buffers |
| `suffix` preservation | Loaders detect file type from extension |
| `delete=False` | Prevents deletion before loader finishes reading |
| `finally: os.unlink()` | Ensures cleanup even if processing fails |

---

## Part 8: Chunking and Indexing

### Creating the Vector Store

```python
if all_documents:
    # Chunk documents
    chunks = chunk_documents(all_documents)
    st.info(f"Created {len(chunks)} chunks from {len(all_documents)} pages")
    
    # Create vector store
    st.session_state.vectorstore = create_vectorstore(chunks)
    save_vectorstore(st.session_state.vectorstore)
    st.success("✅ Documents processed and indexed!")
```

### Chunking Strategy

| Setting | Default Value | Purpose |
|---------|---------------|---------|
| Chunk Size | 800 tokens | Balance between context and precision |
| Chunk Overlap | 200 tokens | Preserve context across boundaries |

### What Happens Here

1. **Chunking** — Documents are split into smaller pieces optimized for embedding and retrieval
2. **Embedding** — Each chunk is converted to a vector (handled inside `create_vectorstore`)
3. **Indexing** — Vectors are added to FAISS for efficient similarity search
4. **Persistence** — Index is saved to disk for future sessions

---

## Part 9: Loaded Documents Display

### Showing Processed Files

```python
# Show loaded documents
if st.session_state.documents_loaded:
    st.markdown("---")
    st.subheader("📁 Loaded Documents")
    for doc in st.session_state.documents_loaded:
        st.text(f"• {doc}")
```

### User Experience Consideration

This section provides visual feedback to users about which documents are currently available for querying. It helps users understand the system's current knowledge base without needing to re-upload files.

---

## Part 10: Settings Display

### Configuration Panel

```python
# Settings
st.markdown("---")
st.header("⚙️ Settings")

try:
    provider = settings.get_active_llm_provider()
    st.success(f"Provider: {provider.upper()}")
except ValueError:
    st.error("No API key configured")

st.text(f"Model: {settings.llm_model}")
st.text(f"Chunk Size: {settings.chunk_size}")
st.text(f"Retrieval K: {settings.retrieval_k}")
```

### Displayed Settings

| Setting | Source | Example Value |
|---------|--------|---------------|
| Provider | Detected from API keys | OPENROUTER |
| Model | `settings.llm_model` | gpt-4o-mini |
| Chunk Size | `settings.chunk_size` | 800 |
| Retrieval K | `settings.retrieval_k` | 4 |

### Error Handling

The `try/except` block gracefully handles the case where no API key is configured, displaying an error message instead of crashing the application.

---

## Part 11: Clear Chat Functionality

### Reset Button

```python
# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
```

### Behavior

1. Clears all messages from session state
2. Triggers a rerun of the application
3. Chat interface resets to empty state

> [!NOTE]
> `st.rerun()` forces a complete script rerun, updating the UI immediately to reflect the cleared state.

---

## Part 12: Main Content Area - Chat Interface

### Chat Title and Initialization

```python
# Main content area
st.title("💬 Chat with Your Documents")

# Load existing vectorstore on startup
if st.session_state.vectorstore is None:
    init_vectorstore()
```

### Lazy Loading

The vector store is only loaded when needed (on first render if `vectorstore` is None). This prevents redundant disk reads on subsequent script reruns.

---

## Part 13: Message History Display

### Rendering Chat Messages

```python
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📖 Sources"):
                for source in message["sources"]:
                    st.markdown(f"**{source['source']}** (Page {source['page']})")
                    st.text(source["content"])
```

### Message Structure

```python
# User message
{
    "role": "user",
    "content": "What is the main topic of the document?"
}

# Assistant message with sources
{
    "role": "assistant",
    "content": "The main topic is...",
    "sources": [
        {
            "source": "report.pdf",
            "page": 3,
            "content": "Relevant chunk text..."
        }
    ]
}
```

### UI Components

| Component | Purpose |
|-----------|---------|
| `st.chat_message()` | Creates styled message bubble (user/assistant) |
| `st.markdown()` | Renders message content with formatting |
| `st.expander()` | Collapsible section for sources |

---

## Part 14: Chat Input and Query Processing

### Handling User Questions

```python
# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Check if vectorstore is loaded
    if st.session_state.vectorstore is None:
        st.warning("⚠️ Please upload and process documents first!")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
```

### The Walrus Operator (`:=`)

The `:=` operator (walrus operator) assigns the input value to `prompt` and checks if it's truthy in one expression. If the user hasn't submitted anything, the block is skipped.

### Validation Flow

```
User enters prompt
        ↓
    ┌───────────────────┐
    │ vectorstore None? │
    └─────────┬─────────┘
         Yes ↓      No ↓
    ┌────────────┐  ┌──────────────┐
    │ Show       │  │ Process      │
    │ Warning    │  │ Query        │
    └────────────┘  └──────────────┘
```

---

## Part 15: RAG Query Execution

### Generating LLM Response

```python
# Generate response
with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
        try:
            result = query_rag(
                st.session_state.vectorstore,
                prompt,
                return_sources=True,
            )
            
            st.markdown(result["answer"])
            
            # Show sources
            if result.get("sources"):
                with st.expander("📖 Sources"):
                    for source in result["sources"]:
                        st.markdown(f"**{source['source']}** (Page {source['page']})")
                        st.text(source["content"])
```

### RAG Query Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      query_rag() Function                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: vectorstore, prompt, return_sources=True                │
│                    ↓                                            │
│  1. Embed the user's question                                   │
│                    ↓                                            │
│  2. Search vectorstore for similar chunks (top-k)               │
│                    ↓                                            │
│  3. Construct prompt with retrieved context                     │
│                    ↓                                            │
│  4. Send to LLM for answer generation                           │
│                    ↓                                            │
│  Output: {"answer": "...", "sources": [...]}                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Result Structure

| Key | Type | Content |
|-----|------|---------|
| `answer` | str | LLM-generated response |
| `sources` | List[dict] | Retrieved chunks with metadata |

---

## Part 16: Saving to Chat History

### Persisting the Response

```python
# Save to history
st.session_state.messages.append({
    "role": "assistant",
    "content": result["answer"],
    "sources": result.get("sources", []),
})
```

### Why Save Sources?

Sources are saved alongside the answer so they remain visible when the page reruns. This allows users to scroll back through their conversation and view the source documents referenced in earlier answers.

---

## Part 17: Error Handling

### Graceful Failure

```python
except Exception as e:
    st.error(f"Error generating response: {e}")
```

### Common Error Scenarios

| Error | Cause | User Sees |
|-------|-------|-----------|
| API timeout | Network issues, overloaded API | "Error generating response: timeout" |
| Invalid API key | Incorrect or expired credentials | "Error generating response: authentication failed" |
| Empty retrieval | No relevant chunks found | May result in generic answer |

---

## Part 18: Empty State Handling

### Guiding New Users

```python
# Empty state
if not st.session_state.messages and st.session_state.vectorstore is None:
    st.info("👆 Upload documents using the sidebar to get started!")
elif not st.session_state.messages:
    st.info("💡 Ask a question about your documents to begin!")
```

### State-Based Messaging

| Condition | Message |
|-----------|---------|
| No vectorstore AND no messages | Guide to upload documents |
| Has vectorstore BUT no messages | Encourage first question |
| Has messages | No empty state message shown |

---

## Full Application Flow Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RAG Document Q&A Application Flow                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐                                                        │
│  │   User Visits    │                                                        │
│  │    app.py        │                                                        │
│  └────────┬─────────┘                                                        │
│           ↓                                                                  │
│  ┌──────────────────┐     ┌─────────────────────────────────────────────┐   │
│  │ Initialize       │     │ Sidebar: Upload Documents                   │   │
│  │ Session State    │────▶│ • Process uploaded files                    │   │
│  └──────────────────┘     │ • Create vectorstore                        │   │
│           ↓               │ • Display settings                          │   │
│  ┌──────────────────┐     └─────────────────────────────────────────────┘   │
│  │ Load Existing    │                                                        │
│  │ Vectorstore      │                                                        │
│  └────────┬─────────┘                                                        │
│           ↓                                                                  │
│  ┌──────────────────┐                                                        │
│  │ Display Chat     │                                                        │
│  │ History          │                                                        │
│  └────────┬─────────┘                                                        │
│           ↓                                                                  │
│  ┌──────────────────┐                                                        │
│  │ User Enters      │                                                        │
│  │ Question         │                                                        │
│  └────────┬─────────┘                                                        │
│           ↓                                                                  │
│  ┌──────────────────┐     ┌─────────────────────────────────────────────┐   │
│  │ Execute RAG      │────▶│ 1. Retrieve relevant chunks                 │   │
│  │ Query            │     │ 2. Send context + question to LLM           │   │
│  └────────┬─────────┘     │ 3. Return answer with sources               │   │
│           ↓               └─────────────────────────────────────────────┘   │
│  ┌──────────────────┐                                                        │
│  │ Display Answer   │                                                        │
│  │ + Sources        │                                                        │
│  └────────┬─────────┘                                                        │
│           ↓                                                                  │
│  ┌──────────────────┐                                                        │
│  │ Save to Chat     │                                                        │
│  │ History          │                                                        │
│  └──────────────────┘                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Running the Application

### Command

```bash
streamlit run app.py
```

### Expected Output

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

### Browser Interface

The application opens in your default browser, presenting the chat interface with the sidebar for document management.

---

## Conclusion

The `app.py` file orchestrates the entire user experience of the RAG Document Q&A System. It demonstrates several key Streamlit patterns:

- **Session state management** for persisting data across reruns
- **Sidebar layout** for organizing secondary controls
- **Chat interface** using `st.chat_message` and `st.chat_input`
- **Progressive disclosure** with expanders for source documents
- **Error handling** for graceful failure modes
- **Empty states** to guide new users

Understanding each component enables you to customize, extend, or debug the application effectively. Whether you're adding new document types, improving the UI, or integrating additional features, this foundation provides a solid starting point.

---

*Document Version: 1.0*  
*Created: January 11, 2026*  
*Reference: Based on `final-plan.md` structure*
