# FAISS Cheat Sheet

*Facebook AI Similarity Search (FAISS) Quick Reference*

---

## Core Concepts

| Term | Definition |
|------|------------|
| **Vector** | List of floats representing text (e.g., `[0.1, -0.5, ...]`) |
| **Index** | Structure optimizing search (like a SQL index) |
| **Dimension** | Length of vectors (OpenAI = 1536) |
| **L2 Distance** | Euclidean distance (lower = more similar) |
| **Inner Product** | Dot product (higher = more similar) |

---

## Operations in `src/vectorstore.py`

### 1. Creating an Index

```python
from langchain_community.vectorstores import FAISS

# Input: Split chunks (List[Document]) + Embedding Model
vectorstore = FAISS.from_documents(chunks, embeddings)
```

### 2. Saving to Disk

```python
# Creates index.faiss and index.pkl
vectorstore.save_local("data/vectorstore")
```

### 3. Loading from Disk

```python
vectorstore = FAISS.load_local(
    "data/vectorstore",
    embeddings,
    allow_dangerous_deserialization=True # Required for pickle
)
```

---

## Search Methods

### Similarity Search

Returns the most similar documents.

```python
# k = number of results
docs = vectorstore.similarity_search("query text", k=4)
```

### Search with Score

Returns documents AND their distance scores.

```python
# Returns List[Tuple[Document, float]]
docs_and_scores = vectorstore.similarity_search_with_score("query", k=4)

for doc, score in docs_and_scores:
    print(f"Distance: {score}") # Lower is better for L2
```

---

## Distance Metrics

FAISS uses different metrics. LangChain's default for OpenAI is usually **L2 (Euclidean)**.

- **L2 Distance**: 0.0 is exact match. Larger is different.
- **Cosine/Inner Product**: 1.0 is exact match. 0.0 is different.

> [!NOTE]
> If you see scores like `0.4` or `0.5`, that's the L2 distance. A score of `0.0` means duplicate text.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `Dimension mismatch` | Embedding model changed | Re-create/overwrite vector store |
| `Index not found` | Path incorrect | Check save location |
| `Serialization error` | Pickle security check | Set `allow_dangerous_deserialization=True` |

---

*Created: January 11, 2026*
