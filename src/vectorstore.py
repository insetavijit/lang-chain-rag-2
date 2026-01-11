"""
FAISS vector store operations.
Handles creation, persistence, and retrieval from the vector store.
"""

from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from src.embeddings import get_embeddings
from src.config import settings


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
