# Learn LCEL: A Practical Guide

*Understanding LangChain Expression Language through `src/chain.py`*

---

## What is LCEL?

LCEL (LangChain Expression Language) is a declarative way to compose chains. It uses the pipe operator (`|`) to link components together, creating a unified `Runnable` object that supports:
- ✅ Streaming (`.stream()`)
- ✅ Async (`.ainvoke()`)
- ✅ Parallel execution
- ✅ Retries and fallbacks

---

## Part 1: The Pipe Concept

In Unix, you pipe commands: `cat file.txt | grep "error" | wc -l`.
In LangChain, you pipe components: `prompt | llm | parser`.

### Your `src/chain.py` Example

```python
chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)
```

Let's break this down step-by-step.

---

## Part 2: Step-by-Step Breakdown

### Step 1: The Parallel Input (`{}`)

The first part of the chain is a dictionary. In LCEL, a dictionary automatically becomes a `RunnableParallel` (or `RunnableMap`). It runs all values in parallel using the **same input**.

```python
{
    "context": retriever | format_docs,
    "question": RunnablePassthrough(),
}
```

If you invoke this with `"What is RAG?"`:

1. **`"question": RunnablePassthrough()`**
   - Takes input "What is RAG?"
   - Returns "What is RAG?" (unchanged)

2. **`"context": retriever | format_docs`**
   - Takes input "What is RAG?"
   - `retriever` searches vector DB → Returns `[Doc1, Doc2]`
   - `|` pipes those docs to `format_docs` function
   - `format_docs` → Returns single string "Content of Doc1..."

**Result (passed to next step):**
```python
{
    "context": "Content of Doc1...",
    "question": "What is RAG?"
}
```

---

## Part 3: The Prompt Template

```python
| prompt
```

The `prompt` object is a `ChatPromptTemplate`. It expects a dictionary with keys matching its variables: `{context}` and `{question}`.

- Input: Dictionary from Step 1
- Action: Fills template placeholders
- Output: `PromptValue` (a list of chat messages)

```
[
  SystemMessage("You are a helpful assistant..."),
  HumanMessage("Context: ...\nQuestion: What is RAG?")
]
```

---

## Part 4: The LLM

```python
| llm
```

The `llm` is `ChatOpenAI`.

- Input: `PromptValue` (messages)
- Action: Calls OpenAI/compatible API
- Output: `AIMessage`

```python
AIMessage(content="RAG stands for Retrieval-Augmented Generation...")
```

---

## Part 5: The Output Parser

```python
| StrOutputParser()
```

- Input: `AIMessage`
- Action: Extracts `.content`
- Output: String

```python
"RAG stands for Retrieval-Augmented Generation..."
```

---

## Part 6: Why Use LCEL?

You could write this in pure Python:

```python
# The "Old" Way (Imperative)
def invoke_chain(question):
    # 1. Retrieve
    docs = retriever.get_relevant_documents(question)
    context = format_docs(docs)
    
    # 2. Prompt
    messages = prompt.format_messages(context=context, question=question)
    
    # 3. LLM
    response = llm.invoke(messages)
    
    # 4. Parse
    return response.content
```

**So why used LCEL?**

1. **Streaming**: `chain.stream(question)` works automatically. The chain streams the LLM output token-by-token.
2. **Async**: `chain.ainvoke(question)` works automatically for non-blocking calls.
3. **Observability**: Tools like LangSmith can visualize the entire chain structure.
4. **Modularity**: You can swap parts easily (e.g., `retriever | other_formatter`).

---

## Part 7: Adding Memory (Future)

To add memory, you'd modify the parallel step:

```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    RunnablePassthrough.assign(
        history=lambda x: x["chat_history"]  # Pass history through
    )
    | {
        "context": itemgetter("question") | retriever | format_docs,
        "question": itemgetter("question"),
        "chat_history": itemgetter("chat_history")
    }
    | prompt_with_history
    | llm
    | StrOutputParser()
)
```

LCEL makes these complex data flows easier to visualize and manage.

---

*Created: January 11, 2026*
