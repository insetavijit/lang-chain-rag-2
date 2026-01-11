# Documentation Index & Restructuring Proposal

## Current Structure Analysis

```
docs/
├── .obsidian/                     # Obsidian config
├── Untitled/                      # Empty - DELETE
├── design/                        # 8 files - component designs
│   ├── app.md
│   ├── chain.md
│   ├── chunker.md
│   ├── config.md
│   ├── embeddings.md
│   ├── loaders.md
│   ├── memory.md
│   └── vectorstore.md
├── learning/                      # Learning materials
│   └── pydentic/                  # 5 files - Pydantic learning
├── planning/                      # 4 files - project planning
│   ├── PH01-walkthrough.md
│   ├── final-plan.md
│   ├── implementation-p1.md
│   └── plan-phase-1.md
├── reference/                     # 5 files - cheatsheets & references
│   ├── cheet-faiss.md
│   ├── cheet-lcel.md
│   ├── langchain-community.md
│   ├── learn-faiss.md
│   └── learn-lcel.md
├── 15Questions-pydantic.md        # Root level - should move
├── README.md
├── mind-maps.md
├── prompt-15GoldenQuestions.txt   # Root level - should move
├── prompt-explore-with-examples.txt
├── rules.md
└── touch-pydentic.md              # Root level - should move
```

## Issues Identified

| Issue | Files Affected |
|-------|----------------|
| Empty directory | `Untitled/` |
| Mixed content at root | Prompts, learning files, questions scattered |
| Inconsistent naming | `cheet-` vs `learn-` prefixes, mixed casing |
| No clear separation | Learning materials mixed with reference |
| Typo in folder name | `pydentic` → `pydantic` |

---

## Proposed Structure

```
docs/
├── index.md                       # This file - documentation hub
├── README.md                      # Docs overview
├── rules.md                       # Project rules
│
├── architecture/                  # System design docs (renamed from design/)
│   ├── overview.md                # High-level architecture
│   ├── app.md
│   ├── chain.md
│   ├── chunker.md
│   ├── config.md
│   ├── embeddings.md
│   ├── loaders.md
│   ├── memory.md
│   └── vectorstore.md
│
├── planning/                      # Project planning (keep as-is)
│   ├── final-plan.md
│   ├── plan-phase-1.md
│   ├── implementation-p1.md
│   └── walkthroughs/
│       └── PH01-walkthrough.md
│
├── guides/                        # Learning & exploration guides
│   ├── pydantic/                  # Fixed typo
│   │   ├── overview.md            # Entry point
│   │   ├── fundamentals.md
│   │   ├── questions.md           # Interview questions
│   │   └── settings.md
│   ├── langchain/
│   │   ├── lcel.md
│   │   └── community.md
│   └── faiss/
│       └── overview.md
│
├── reference/                     # Quick reference & cheatsheets
│   ├── pydantic-cheatsheet.md
│   ├── lcel-cheatsheet.md
│   ├── faiss-cheatsheet.md
│   └── langchain-community.md
│
├── prompts/                       # Reusable prompts
│   ├── 15-golden-questions.txt
│   └── explore-with-examples.txt
│
└── assets/                        # Diagrams, images, exports
    └── mind-maps.md
```

---

## Migration Plan

### Step 1: Create New Directories
```bash
mkdir docs/architecture
mkdir docs/guides
mkdir docs/guides/pydantic
mkdir docs/guides/langchain
mkdir docs/guides/faiss
mkdir docs/prompts
mkdir docs/assets
mkdir docs/planning/walkthroughs
```

### Step 2: Move & Rename Files

| From | To |
|------|-----|
| `design/*` | `architecture/*` |
| `learning/pydentic/*` | `guides/pydantic/*` |
| `reference/learn-lcel.md` | `guides/langchain/lcel.md` |
| `reference/learn-faiss.md` | `guides/faiss/overview.md` |
| `reference/cheet-lcel.md` | `reference/lcel-cheatsheet.md` |
| `reference/cheet-faiss.md` | `reference/faiss-cheatsheet.md` |
| `prompt-15GoldenQuestions.txt` | `prompts/15-golden-questions.txt` |
| `prompt-explore-with-examples.txt` | `prompts/explore-with-examples.txt` |
| `15Questions-pydantic.md` | `guides/pydantic/questions.md` |
| `touch-pydentic.md` | `guides/pydantic/fundamentals.md` |
| `mind-maps.md` | `assets/mind-maps.md` |
| `planning/PH01-walkthrough.md` | `planning/walkthroughs/PH01-walkthrough.md` |

### Step 3: Cleanup
```bash
rmdir docs/Untitled
rmdir docs/design
rmdir docs/learning/pydentic
rmdir docs/learning
```

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Directories | lowercase, singular | `guide/`, `reference/` |
| Guide files | descriptive, lowercase | `fundamentals.md`, `overview.md` |
| Cheatsheets | `{topic}-cheatsheet.md` | `lcel-cheatsheet.md` |
| Questions | `questions.md` in topic folder | `pydantic/questions.md` |
| Prompts | descriptive with `.txt` | `explore-with-examples.txt` |
| Walkthroughs | `{phase}-walkthrough.md` | `PH01-walkthrough.md` |

---

## Quick Navigation

### By Purpose

| I want to... | Go to |
|--------------|-------|
| Understand system design | `architecture/` |
| Learn a new topic | `guides/{topic}/` |
| Quick reference/lookup | `reference/` |
| See project plans | `planning/` |
| Use a prompt template | `prompts/` |

### By Topic

| Topic | Guide | Cheatsheet |
|-------|-------|------------|
| Pydantic | `guides/pydantic/` | `reference/pydantic-cheatsheet.md` |
| LangChain LCEL | `guides/langchain/lcel.md` | `reference/lcel-cheatsheet.md` |
| FAISS | `guides/faiss/overview.md` | `reference/faiss-cheatsheet.md` |
| RAG Components | `architecture/` | - |
