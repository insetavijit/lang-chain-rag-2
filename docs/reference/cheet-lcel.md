# LCEL Cheat Sheet

*LangChain Expression Language (LCEL) Quick Reference*

---

## The Pipe Operator (`|`)

The core of LCEL. It takes the output of the left side and feeds it as input to the right side.

```python
# A simple chain
chain = prompt | model | output_parser

# Equivalent to function calls:
# output_parser(model(prompt(input)))
```

---

## Basic Building Blocks

| Component | Purpose | Input | Output |
|-----------|---------|-------|--------|
| `PromptTemplate` | Format text | Dictionary | PromptValue |
| `ChatModel` | Generate text | PromptValue | AIMessage |
| `StrOutputParser` | Extract string | AIMessage | String |

### Example Chain

```python
chain = (
    ChatPromptTemplate.from_template("Tell me a joke about {topic}")
    | ChatOpenAI()
    | StrOutputParser()
)

chain.invoke({"topic": "bears"})
# Result: "Why did the bear..."
```

---

## Parallel Execution (RunnableMap)

Use a dictionary to run components in parallel and merge results.

```python
chain = (
    {
        "context": retriever,        # 1. Fetch docs
        "question": RunnablePassthrough() # 2. Pass question through
    }
    | prompt
    | model
)
```

**Flow:**
```
Input: "What is RAG?"
      ↓
┌─────────────┬─────────────────────┐
│ "context"   │ "question"          │
│ Retriever   │ RunnablePassthrough │
│ (Docs...)   │ ("What is RAG?")    │
└─────────────┴─────────────────────┘
      ↓
Result: {"context": [Docs...], "question": "What is RAG?"}
      ↓
    Prompt
```

---

## Key Runnables

### 1. RunnablePassthrough

Passes the input unchanged to the next step. Essential for dict keys that need the raw input.

```python
from langchain_core.runnables import RunnablePassthrough

# Pass input as 'question'
{"question": RunnablePassthrough()}
```

### 2. RunnableLambda

Wrap any Python function as a runnable step.

```python
from langchain_core.runnables import RunnableLambda

def length_func(text):
    return len(text)

chain = RunnableLambda(length_func)
chain.invoke("hello") # 5
```

---

## Common patterns in RAG

```python
# The RAG Chain Recipe
rag_chain = (
    {
        "context": retriever | format_docs,  # Fetch & Format
        "question": RunnablePassthrough()    # Pass input
    }
    | prompt      # Insert context & question
    | llm         # Generate answer
    | parse       # Extract string
)
```

---

*Created: January 11, 2026*
