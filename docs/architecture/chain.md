# Chain Module: Complete Guide

*RAG chain implementation combining retrieval and generation*

**File**: `src/chain.py` | **Purpose**: Orchestrate the RAG pipeline

---

## Introduction

The `chain.py` module is the heart of the RAG system—it orchestrates the entire question-answering pipeline by connecting retrieval with generation. Using LangChain Expression Language (LCEL), it creates a composable chain that retrieves relevant documents, formats them as context, and generates answers using an LLM.

---

## Part 1: Module Imports

### Dependencies

```python
from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from src.config import settings
from src.vectorstore import similarity_search
```

| Import | Purpose |
|--------|---------|
| `ChatOpenAI` | LLM client for OpenAI-compatible APIs |
| `ChatPromptTemplate` | Structured prompt creation |
| `StrOutputParser` | Extract string from LLM response |
| `RunnablePassthrough` | Pass input unchanged through chain |
| `similarity_search` | Retrieve relevant documents |

---

## Part 2: RAG Prompt Template

### Prompt Definition

```python
RAG_PROMPT = """You are a helpful assistant that answers questions based on the provided context.
Use the following pieces of context to answer the question. If you don't know the answer based on the context, say "I don't have enough information to answer this question."

Always cite your sources by mentioning which document the information came from.

Context:
{context}

Question: {question}

Answer:"""
```

### Prompt Variables

| Variable | Source | Purpose |
|----------|--------|---------|
| `{context}` | Retrieved documents | Provides grounding information |
| `{question}` | User input | The question to answer |

### Prompt Design Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                     RAG Prompt Structure                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. ROLE DEFINITION                                              │
│     "You are a helpful assistant..."                            │
│     └─→ Sets behavior expectations                              │
│                                                                  │
│  2. GROUNDING INSTRUCTION                                        │
│     "Use the following pieces of context..."                    │
│     └─→ Limits to provided information                          │
│                                                                  │
│  3. FALLBACK HANDLING                                            │
│     "If you don't know...say 'I don't have enough...'"         │
│     └─→ Prevents hallucination                                  │
│                                                                  │
│  4. CITATION REQUIREMENT                                         │
│     "Always cite your sources..."                               │
│     └─→ Ensures traceability                                    │
│                                                                  │
│  5. CONTEXT INJECTION                                            │
│     "{context}"                                                 │
│     └─→ Dynamic document content                                │
│                                                                  │
│  6. USER QUESTION                                                │
│     "{question}"                                                │
│     └─→ What user wants answered                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 3: LLM Factory Function

### get_llm()

```python
def get_llm(
    model: Optional[str] = None,
    temperature: float = 0.0,
    streaming: bool = True,
) -> ChatOpenAI:
    """
    Get configured LLM instance.
    
    Args:
        model: Model name (uses config default if None)
        temperature: Sampling temperature (0.0 = deterministic)
        streaming: Enable streaming responses
        
    Returns:
        ChatOpenAI instance configured for the active provider
    """
    return ChatOpenAI(
        model=model or settings.llm_model,
        temperature=temperature,
        streaming=streaming,
        openai_api_key=settings.get_llm_api_key(),
        openai_api_base=settings.get_llm_base_url(),
    )
```

### Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `model` | gpt-4o-mini | Which model to use |
| `temperature` | 0.0 | Deterministic for RAG (no randomness) |
| `streaming` | True | Enable token-by-token streaming |

### Temperature Guidance

| Temperature | Use Case |
|-------------|----------|
| 0.0 | RAG, factual Q&A (no creativity) |
| 0.3-0.5 | Balanced responses |
| 0.7-1.0 | Creative writing |

---

## Part 4: Document Formatting

### format_docs()

```python
def format_docs(docs: List[Document]) -> str:
    """
    Format retrieved documents into a single context string.
    
    Args:
        docs: List of retrieved documents
        
    Returns:
        Formatted context string with source citations
    """
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        formatted.append(
            f"[Document {i} - {source} (Page {page})]:\n{doc.page_content}"
        )
    return "\n\n---\n\n".join(formatted)
```

### Output Format

```
[Document 1 - report.pdf (Page 3)]:
Machine learning is a subset of artificial intelligence that enables
systems to learn and improve from experience without being explicitly
programmed...

---

[Document 2 - report.pdf (Page 7)]:
Deep learning, a type of machine learning, uses neural networks with
many layers to analyze various factors of data...

---

[Document 3 - notes.txt (Page N/A)]:
Key concepts in ML include supervised learning, unsupervised learning,
and reinforcement learning...
```

---

## Part 5: RAG Chain Creation

### create_rag_chain()

```python
def create_rag_chain(vectorstore: FAISS):
    """
    Create a RAG chain with retrieval and generation.
    
    Args:
        vectorstore: FAISS vector store for retrieval
        
    Returns:
        Runnable chain that takes a question and returns an answer
    """
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT)
    
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": settings.retrieval_k}
    )
    
    # Build the chain
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain
```

### LCEL Chain Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        LCEL Chain Flow                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: "What is machine learning?"                             │
│                   │                                              │
│                   ▼                                              │
│  ┌─────────────────────────────────────────┐                    │
│  │         Parallel Execution               │                    │
│  │  ┌─────────────────────────────────┐    │                    │
│  │  │ "context": retriever|format_docs│    │                    │
│  │  │     └─→ Search + Format         │    │                    │
│  │  └─────────────────────────────────┘    │                    │
│  │  ┌─────────────────────────────────┐    │                    │
│  │  │ "question": RunnablePassthrough │    │                    │
│  │  │     └─→ Pass question unchanged │    │                    │
│  │  └─────────────────────────────────┘    │                    │
│  └─────────────────────────────────────────┘                    │
│                   │                                              │
│                   ▼                                              │
│  {"context": "...", "question": "What is ML?"}                  │
│                   │                                              │
│                   ▼                                              │
│  ┌─────────────────────────────────────────┐                    │
│  │            prompt                        │                    │
│  │    Format into ChatPromptTemplate       │                    │
│  └─────────────────────────────────────────┘                    │
│                   │                                              │
│                   ▼                                              │
│  ┌─────────────────────────────────────────┐                    │
│  │             llm                          │                    │
│  │    Send to ChatOpenAI                   │                    │
│  └─────────────────────────────────────────┘                    │
│                   │                                              │
│                   ▼                                              │
│  ┌─────────────────────────────────────────┐                    │
│  │        StrOutputParser()                 │                    │
│  │    Extract text from response           │                    │
│  └─────────────────────────────────────────┘                    │
│                   │                                              │
│                   ▼                                              │
│  Output: "Machine learning is a subset of AI that..."          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 6: RAG Query Function

### query_rag()

```python
def query_rag(
    vectorstore: FAISS,
    question: str,
    return_sources: bool = False,
) -> Dict[str, Any]:
    """
    Query the RAG system with a question.
    
    Args:
        vectorstore: FAISS vector store
        question: User's question
        return_sources: Whether to include source documents
        
    Returns:
        Dictionary with 'answer' and optionally 'sources'
    """
    # Get relevant documents
    docs = similarity_search(vectorstore, question)
    
    # Create and invoke chain
    chain = create_rag_chain(vectorstore)
    answer = chain.invoke(question)
    
    result = {"answer": answer}
    
    if return_sources:
        result["sources"] = [
            {
                "content": doc.page_content[:200] + "...",
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A"),
            }
            for doc in docs
        ]
    
    return result
```

### Return Structure

```python
# Without sources
{
    "answer": "Machine learning is a subset of artificial intelligence..."
}

# With sources (return_sources=True)
{
    "answer": "Machine learning is a subset of artificial intelligence...",
    "sources": [
        {
            "content": "Machine learning is a subset of artificial...",
            "source": "report.pdf",
            "page": 3
        },
        {
            "content": "Deep learning, a type of machine learning...",
            "source": "report.pdf", 
            "page": 7
        }
    ]
}
```

---

## Part 7: Async Query Function

### aquery_rag()

```python
async def aquery_rag(
    vectorstore: FAISS,
    question: str,
    return_sources: bool = False,
) -> Dict[str, Any]:
    """
    Async version of query_rag.
    
    Args:
        vectorstore: FAISS vector store
        question: User's question
        return_sources: Whether to include source documents
        
    Returns:
        Dictionary with 'answer' and optionally 'sources'
    """
    docs = similarity_search(vectorstore, question)
    chain = create_rag_chain(vectorstore)
    answer = await chain.ainvoke(question)
    
    result = {"answer": answer}
    
    if return_sources:
        result["sources"] = [
            {
                "content": doc.page_content[:200] + "...",
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A"),
            }
            for doc in docs
        ]
    
    return result
```

### When to Use Async

| Use Case | Method |
|----------|--------|
| Streamlit app (sync) | `query_rag()` |
| FastAPI endpoint | `aquery_rag()` |
| Concurrent queries | `aquery_rag()` |
| Jupyter notebooks | Either works |

---

## Usage Examples

### Basic Query

```python
from src.vectorstore import load_vectorstore
from src.chain import query_rag

vectorstore = load_vectorstore()
result = query_rag(vectorstore, "What is the main conclusion?")
print(result["answer"])
```

### With Sources

```python
result = query_rag(
    vectorstore,
    "Explain the methodology",
    return_sources=True
)

print(f"Answer: {result['answer']}\n")
print("Sources:")
for src in result["sources"]:
    print(f"  - {src['source']} (Page {src['page']})")
```

### Custom LLM Settings

```python
from src.chain import get_llm

# Higher temperature for creative responses
llm = get_llm(temperature=0.7, streaming=False)
response = llm.invoke("Write a poem about machine learning")
```

### Direct Chain Usage

```python
from src.chain import create_rag_chain

chain = create_rag_chain(vectorstore)

# Streaming
for chunk in chain.stream("What is AI?"):
    print(chunk, end="", flush=True)
```

---

## Integration with RAG Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG Pipeline                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────┐                                   │
│  │   vectorstore.py         │                                   │
│  │  similarity_search()     │                                   │
│  └────────────┬─────────────┘                                   │
│               ↓                                                  │
│  ┌──────────────────────────┐                                   │
│  │      chain.py            │ ◄── YOU ARE HERE                  │
│  │  create_rag_chain()     │                                   │
│  │  query_rag()            │                                   │
│  └────────────┬─────────────┘                                   │
│               ↓                                                  │
│  ┌──────────────────────────┐                                   │
│  │       app.py             │                                   │
│  │  (Streamlit interface)   │                                   │
│  └──────────────────────────┘                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Document Version: 1.0*  
*Created: January 11, 2026*
