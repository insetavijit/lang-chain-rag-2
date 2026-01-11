"""
RAG Document Q&A System - Streamlit Application

Main entry point for the Streamlit web interface.
Run with: streamlit run app.py
"""

import streamlit as st
from pathlib import Path
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

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


# Initialize session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = []
if "messages" not in st.session_state:
    st.session_state.messages = []


def init_vectorstore():
    """Load existing vectorstore if available."""
    if vectorstore_exists():
        try:
            st.session_state.vectorstore = load_vectorstore()
            return True
        except Exception as e:
            st.error(f"Failed to load vector store: {e}")
    return False


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
                
                if all_documents:
                    # Chunk documents
                    chunks = chunk_documents(all_documents)
                    st.info(f"Created {len(chunks)} chunks from {len(all_documents)} pages")
                    
                    # Create vector store
                    st.session_state.vectorstore = create_vectorstore(chunks)
                    save_vectorstore(st.session_state.vectorstore)
                    st.success("✅ Documents processed and indexed!")
    
    # Show loaded documents
    if st.session_state.documents_loaded:
        st.markdown("---")
        st.subheader("📁 Loaded Documents")
        for doc in st.session_state.documents_loaded:
            st.text(f"• {doc}")
    
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
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# Main content area
st.title("💬 Chat with Your Documents")

# Load existing vectorstore on startup
if st.session_state.vectorstore is None:
    init_vectorstore()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📖 Sources"):
                for source in message["sources"]:
                    st.markdown(f"**{source['source']}** (Page {source['page']})")
                    st.text(source["content"])

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
                    
                    # Save to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result.get("sources", []),
                    })
                    
                except Exception as e:
                    st.error(f"Error generating response: {e}")

# Empty state
if not st.session_state.messages and st.session_state.vectorstore is None:
    st.info("👆 Upload documents using the sidebar to get started!")
elif not st.session_state.messages:
    st.info("💡 Ask a question about your documents to begin!")
