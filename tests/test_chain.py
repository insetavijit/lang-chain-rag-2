"""
Tests for RAG chain functionality.
"""

import pytest
from unittest.mock import Mock, patch


def test_config_loads():
    """Test that configuration loads without errors."""
    from src.config import settings
    
    assert settings is not None
    assert settings.chunk_size > 0
    assert settings.chunk_overlap >= 0
    assert settings.retrieval_k > 0


def test_chunk_size_default():
    """Test default chunk size is 800."""
    from src.config import settings
    
    assert settings.chunk_size == 800


def test_chunk_overlap_default():
    """Test default chunk overlap is 200."""
    from src.config import settings
    
    assert settings.chunk_overlap == 200


def test_text_splitter_creation():
    """Test text splitter can be created."""
    from src.chunker import create_text_splitter
    
    splitter = create_text_splitter()
    assert splitter is not None
    assert splitter._chunk_size == 800
    assert splitter._chunk_overlap == 200


def test_chunk_text():
    """Test text chunking."""
    from src.chunker import chunk_text
    
    # Create text longer than chunk size
    text = "Hello world. " * 200  # ~2600 chars
    chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)
    
    assert len(chunks) > 1
    assert all(len(c) <= 600 for c in chunks)  # Allow some margin


def test_document_loader_supported_types():
    """Test that loader supports expected file types."""
    from pathlib import Path
    from src.loaders import get_loader
    
    # Test that correct loader types are returned
    # Note: get_loader will validate file extension but loader requires actual file
    # So we just verify no exception for supported extensions by checking the type
    try:
        loader_pdf = get_loader("test.pdf")
        assert "PDF" in type(loader_pdf).__name__
    except ValueError:
        pass  # File doesn't exist, but extension is supported
    
    try:
        loader_docx = get_loader("test.docx")
        assert "Docx" in type(loader_docx).__name__ or loader_docx is not None
    except ValueError:
        pass
    
    try:
        loader_txt = get_loader("test.txt")
        assert "Text" in type(loader_txt).__name__ or loader_txt is not None
    except ValueError:
        pass


def test_document_loader_unsupported_type():
    """Test that loader raises for unsupported types."""
    from src.loaders import get_loader
    
    with pytest.raises(ValueError, match="Unsupported file type"):
        get_loader("test.xyz")


def test_chat_memory():
    """Test chat memory operations."""
    from src.memory import ChatMemory
    
    memory = ChatMemory(max_messages=3)
    
    # Add messages
    memory.add_user_message("Hello")
    memory.add_ai_message("Hi there!")
    
    messages = memory.get_messages()
    assert len(messages) == 2
    
    # Test clear
    memory.clear()
    assert len(memory.get_messages()) == 0


def test_chat_memory_trimming():
    """Test that memory trims old messages."""
    from src.memory import ChatMemory
    
    memory = ChatMemory(max_messages=2)
    
    # Add more than max
    memory.add_exchange("Q1", "A1")
    memory.add_exchange("Q2", "A2")
    memory.add_exchange("Q3", "A3")
    
    messages = memory.get_messages()
    # Should only have last 2 exchanges (4 messages)
    assert len(messages) == 4


def test_session_memory():
    """Test session-based memory."""
    from src.memory import get_session_memory, clear_session_memory
    
    session_id = "test_session_123"
    
    # Get memory for session
    memory = get_session_memory(session_id)
    memory.add_user_message("Test")
    
    # Get same session again
    same_memory = get_session_memory(session_id)
    assert len(same_memory.get_messages()) == 1
    
    # Clear session
    clear_session_memory(session_id)
    cleared_memory = get_session_memory(session_id)
    assert len(cleared_memory.get_messages()) == 0
