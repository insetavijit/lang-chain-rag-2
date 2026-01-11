"""
Document loaders for PDF, DOCX, and TXT files.
Provides unified interface for loading various document types.
"""

from pathlib import Path
from typing import List, Union
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)


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
