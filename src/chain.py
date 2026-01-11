"""
RAG chain implementation.
Combines retrieval and generation for question answering.
"""

from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from src.config import settings
from src.vectorstore import similarity_search


# RAG Prompt Template
RAG_PROMPT = """You are a helpful assistant that answers questions based on the provided context.
Use the following pieces of context to answer the question. If you don't know the answer based on the context, say "I don't have enough information to answer this question."

Always cite your sources by mentioning which document the information came from.

Context:
{context}

Question: {question}

Answer:"""


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
    # Get relevant documents
    docs = similarity_search(vectorstore, question)
    
    # Create and invoke chain
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
