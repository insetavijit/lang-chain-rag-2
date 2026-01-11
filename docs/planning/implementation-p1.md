# Phase 1 Implementation Tasks

*A step-by-step task list for implementing the RAG Document Q&A System foundation*

**Estimated Time**: 2 days | **Total Tasks**: 35

---

## Overview

This document breaks down Phase 1 into actionable tasks. Each task includes a brief description of what needs to be done. Work through these sequentially, checking off items as you complete them.

---

## 1. Repository Setup

| # | Task | Brief |
|---|------|-------|
| 1.1 | Create GitHub repository | Go to GitHub → New Repository → Name: `rag-document-qa` → Public → Add README → MIT License |
| 1.2 | Clone repository locally | Run `git clone <repo-url>` in your workspace directory |
| 1.3 | Create `.gitignore` | Add Python, venv, .env, data/, IDE ignores (use template from final-plan.md) |
| 1.4 | Create project folders | Create `src/`, `notebooks/`, `data/`, `data/documents/`, `data/vectorstore/`, `tests/` directories |
| 1.5 | Create `src/__init__.py` | Empty file to make src a Python package |
| 1.6 | Create `tests/__init__.py` | Empty file to make tests a Python package |
| 1.7 | Create `.env.example` | Copy template from final-plan.md with placeholder values |
| 1.8 | Create placeholder README | Add project title, brief description, "Setup instructions coming soon" |
| 1.9 | Initial commit | `git add .` → `git commit -m "Initial project structure"` → `git push` |

---

## 2. Python Environment

| # | Task | Brief |
|---|------|-------|
| 2.1 | Verify Python version | Run `python --version` — must be 3.10 or higher |
| 2.2 | Install uv (optional) | Run `pip install uv` if using uv package manager |
| 2.3 | Create virtual environment | Run `uv venv` OR `python -m venv .venv` |
| 2.4 | Activate virtual environment | Windows: `.venv\Scripts\activate` — Linux/Mac: `source .venv/bin/activate` |
| 2.5 | Create `pyproject.toml` | Copy from final-plan.md with all dependencies listed |
| 2.6 | Create `requirements.txt` | Copy from final-plan.md as backup/alternative |
| 2.7 | Install dependencies | Run `uv pip install -e .` OR `pip install -r requirements.txt` |
| 2.8 | Verify core imports | Open Python REPL → `import langchain, faiss, streamlit` — no errors = success |
| 2.9 | Commit environment files | `git add pyproject.toml requirements.txt` → commit → push |

---

## 3. API Keys & Configuration

| # | Task | Brief |
|---|------|-------|
| 3.1 | Get OpenRouter API key | Go to openrouter.ai → Sign up → Dashboard → API Keys → Create new key |
| 3.2 | Get Groq API key (backup) | Go to console.groq.com → Sign up → API Keys → Create new key |
| 3.3 | Get Langfuse keys (optional) | Go to cloud.langfuse.com → Sign up → Settings → API Keys |
| 3.4 | Create `.env` file | Copy `.env.example` to `.env` → Fill in your actual API keys |
| 3.5 | Verify `.env` is gitignored | Run `git status` — `.env` should NOT appear in untracked files |
| 3.6 | Create `src/config.py` | Copy the Pydantic Settings class from final-plan.md |
| 3.7 | Test config loading | Python REPL → `from src.config import settings` → `print(settings.llm_model)` |
| 3.8 | Commit config module | `git add src/config.py` → commit → push (NOT .env!) |

---

## 4. Jupyter Notebook Setup

| # | Task | Brief |
|---|------|-------|
| 4.1 | Register Jupyter kernel | Run `python -m ipykernel install --user --name=rag-document-qa --display-name="RAG Document QA"` |
| 4.2 | Create `.vscode` folder | Create `.vscode/` directory in project root |
| 4.3 | Create VS Code settings | Create `.vscode/settings.json` with Jupyter config from final-plan.md |
| 4.4 | Create exploration notebook | Create `notebooks/01_exploration.ipynb` — can be empty initially |
| 4.5 | Create RAG testing notebook | Create `notebooks/02_rag_testing.ipynb` — can be empty initially |
| 4.6 | Test notebook kernel | Open notebook in VS Code → Select "RAG Document QA" kernel → Run `print("Hello")` |
| 4.7 | Commit notebook setup | `git add notebooks/ .vscode/` → commit → push |

---

## 5. API Connection Test

| # | Task | Brief |
|---|------|-------|
| 5.1 | Open exploration notebook | Open `notebooks/01_exploration.ipynb` in VS Code |
| 5.2 | Add environment check cell | Add cell with dotenv load + API key verification (from final-plan.md) |
| 5.3 | Run environment check | Execute cell — should show ✓ for configured keys |
| 5.4 | Add LLM test cell | Add cell with ChatOpenAI test call (from final-plan.md) |
| 5.5 | Run LLM test | Execute cell — should receive response from model |
| 5.6 | Document any errors | If errors occur, note them and troubleshoot before proceeding |
| 5.7 | Commit working notebook | `git add notebooks/` → commit "Verified API connection" → push |

---

## 6. Create Placeholder Source Files

| # | Task | Brief |
|---|------|-------|
| 6.1 | Create `src/loaders.py` | Add file with docstring: `"""Document loading utilities."""` + `pass` |
| 6.2 | Create `src/chunker.py` | Add file with docstring: `"""Text chunking utilities."""` + `pass` |
| 6.3 | Create `src/embeddings.py` | Add file with docstring: `"""Embedding generation."""` + `pass` |
| 6.4 | Create `src/vectorstore.py` | Add file with docstring: `"""FAISS vector store operations."""` + `pass` |
| 6.5 | Create `src/chain.py` | Add file with docstring: `"""RAG chain implementation."""` + `pass` |
| 6.6 | Create `src/memory.py` | Add file with docstring: `"""Conversation memory."""` + `pass` |
| 6.7 | Create `app.py` | Add file with basic Streamlit hello world: `import streamlit as st; st.title("RAG Q&A")` |
| 6.8 | Create `tests/test_chain.py` | Add file with placeholder: `"""Tests for RAG chain."""` + `def test_placeholder(): pass` |
| 6.9 | Test Streamlit runs | Run `streamlit run app.py` — should open browser with title |
| 6.10 | Commit all source files | `git add src/ app.py tests/` → commit "Add source file placeholders" → push |

---

## 7. Final Verification

| # | Task | Brief |
|---|------|-------|
| 7.1 | Verify folder structure | Run `tree` or `ls -la` — confirm matches plan structure |
| 7.2 | Verify all imports | Python REPL → import each src module → no errors |
| 7.3 | Verify Streamlit works | `streamlit run app.py` → page loads in browser |
| 7.4 | Verify notebook works | Run all cells in exploration notebook → API responds |
| 7.5 | Update README | Add setup instructions, project description, tech stack |
| 7.6 | Final commit | `git add .` → commit "Phase 1 complete" → push |
| 7.7 | Tag release | `git tag v0.1.0-phase1` → `git push --tags` |

---

## Quick Reference: Commands

### Environment Setup
```bash
# Create and activate environment
uv venv                          # or: python -m venv .venv
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # Linux/Mac

# Install dependencies
uv pip install -e .              # or: pip install -r requirements.txt

# Register Jupyter kernel
python -m ipykernel install --user --name=rag-document-qa --display-name="RAG Document QA"
```

### Git Commands
```bash
# Initial setup
git clone <repo-url>
git add .
git commit -m "Initial project structure"
git push

# Regular commits
git add <files>
git commit -m "message"
git push

# Tag release
git tag v0.1.0-phase1
git push --tags
```

### Testing
```bash
# Test Streamlit
streamlit run app.py

# Test imports
python -c "from src.config import settings; print(settings.llm_model)"

# Test dependencies
python -c "import langchain, faiss, streamlit, openai; print('All imports OK')"
```

---

## Completion Checklist

Use this final checklist to verify Phase 1 is complete:

| ✓ | Criteria |
|---|----------|
| ☐ | GitHub repository created with proper structure |
| ☐ | Virtual environment created and activated |
| ☐ | All dependencies installed without errors |
| ☐ | API keys configured in `.env` file |
| ☐ | `.env` is gitignored (not committed) |
| ☐ | `src/config.py` loads settings correctly |
| ☐ | Jupyter kernel registered and working |
| ☐ | Exploration notebook runs successfully |
| ☐ | LLM API call returns valid response |
| ☐ | Streamlit app launches without errors |
| ☐ | All placeholder source files created |
| ☐ | README updated with project info |
| ☐ | All changes committed and pushed |

---

## Next: Phase 2

Once all tasks above are complete, proceed to **Phase 2: Document Processing Pipeline**:

- Implement PDF, DOCX, TXT loaders in `src/loaders.py`
- Build chunking logic in `src/chunker.py`
- Create embedding functions in `src/embeddings.py`
- Set up FAISS in `src/vectorstore.py`

---

*Document Version: 1.0*  
*Created: January 11, 2026*
