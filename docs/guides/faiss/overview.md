# Learn FAISS: A Practical Guide

*Understanding Vector Databases through `src/vectorstore.py`*

---

## What is FAISS?

FAISS (Facebook AI Similarity Search) is a library that allows you to quickly search for "similar" vectors in huge datasets.
In our RAG system, it acts as the **Long-Term Memory**.

---

## Part 1: The Vector Concept

Machines can't understand text directly. They understand numbers.
An **Embedding Model** (like OpenAI's `text-embedding-3-small`) converts text into a list of 1,536 numbers.

```
"Cat"  → [0.001, 0.052, -0.021, ...]
"Dog"  → [0.002, 0.051, -0.019, ...]  ← Similar numbers
"Car"  → [0.890, -0.120, 0.440, ...]  ← Different numbers
```

FAISS stores these lists and calculates how "close" they are to each other.

---

## Part 2: Creation Workflow (`create_vectorstore`)

```python
# src/vectorstore.py

def create_vectorstore(documents):
    embeddings = get_embeddings() # 1. Get model
    vectorstore = FAISS.from_documents(documents, embeddings) # 2. Build index
    return vectorstore
```

**What happens inside:**
1. **Embed**: It sends every document chunk to OpenAI API.
2. **Collect**: It gets back 1,536 floats for each chunk.
3. **Index**: It builds a data structure (matrix) in RAM that makes comparing them fast.

---

## Part 3: Search Workflow (`similarity_search`)

When a user asks "How do I reset my password?":

1. **Embed Query**: "How do I reset my password?" → `[0.5, -0.1, ...]`
2. **Scan Index**: FAISS compares this query vector against all stored doc vectors.
3. **Rank**: It finds the top `k` (e.g., 4) closest vectors.
4. **Retrieve**: It looks up the original text associated with those vectors.

---

## Part 4: Persistence (`save/load`)

FAISS is an **in-memory** database. If you stop the script, it vanishes.
That's why `save_vectorstore` is crucial.

```python
# Saves two files:
# 1. index.faiss (The heavy math matrix)
# 2. index.pkl   (The text content + metadata mapping)
```

When `app.py` starts, it calls `load_vectorstore()` to bring these files back into RAM so you don't have to pay for embeddings again.

---

## Part 5: Why FAISS?

| Feature | FAISS (Local) | Pinecone/Weaviate (Cloud) |
|---------|---------------|---------------------------|
| **Cost** | Free | Paid / Tiered |
| **Privacy** | Data stays on disk | Data sent to cloud |
| **Setup** | `pip install` | Sign up, keys, config |
| **Scale** | Good for <1M docs | Good for 1B+ docs |

For a local RAG app like this, **FAISS is perfect**: zero cost, fast, and private.

---

## Part 6: Best Practices

1. **Chunk Size Matters**: 
   - Too small? Vectors miss context.
   - Too big? Vectors get "diluted" (averaging too many topics).
   - Our setting: **800 chars** (Sweet spot).

2. **Refreshes**:
   - If you change the embedding model, you **MUST** delete and recreate the vector store. Vectors from different models are like apples and oranges.

3. **Metadata**:
   - We store `source` and `page` in the metadata so we can cite sources later. FAISS keeps this safe alongside the vectors.

---

*Created: January 11, 2026*
