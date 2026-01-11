"""
Embedding generation for document vectors.
Supports OpenAI embeddings via OpenRouter or direct API.
"""

from typing import List
from langchain_openai import OpenAIEmbeddings
from src.config import settings


def get_embeddings() -> OpenAIEmbeddings:
    """
    Get configured embedding model instance.
    
    Returns:
        OpenAIEmbeddings instance configured for the active provider
    """
    provider = settings.get_active_llm_provider()
    
    # OpenRouter and Groq don't support embeddings, use OpenAI directly
    # For OpenRouter users, we assume they also have OpenAI access for embeddings
    # or we can use a fallback
    
    if provider == "openrouter":
        # OpenRouter supports OpenAI embeddings through their API
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
        # Fallback: Try OpenRouter if available, otherwise error
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
