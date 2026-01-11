# Memory Module: Complete Guide

*Conversation history management for multi-turn dialogues*

**File**: `src/memory.py` | **Purpose**: Maintain context across chat turns

---

## Introduction

The `memory.py` module provides conversation memory capabilities for the RAG system. Memory enables multi-turn dialogues where the system can reference previous exchanges, making conversations feel natural and contextual. This module implements a simple but effective memory manager that stores and retrieves chat history.

---

## Part 1: Module Imports

### Dependencies

```python
from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
```

| Import | Purpose |
|--------|---------|
| `List, Dict, Optional` | Type hints |
| `HumanMessage` | Represents user messages |
| `AIMessage` | Represents assistant messages |
| `BaseMessage` | Base class for all message types |

---

## Part 2: ChatMemory Class

### Class Definition

```python
class ChatMemory:
    """
    Simple chat memory manager for storing conversation history.
    """
    
    def __init__(self, max_messages: Optional[int] = None):
        """
        Initialize chat memory.
        
        Args:
            max_messages: Maximum number of message pairs to keep (None = unlimited)
        """
        self.max_messages = max_messages
        self.messages: List[BaseMessage] = []
```

### Memory Configuration

| Parameter | Default | Effect |
|-----------|---------|--------|
| `max_messages` | None | Unlimited history |
| `max_messages=5` | 5 pairs | Keeps last 5 exchanges (10 messages) |
| `max_messages=10` | 10 pairs | Keeps last 10 exchanges (20 messages) |

---

## Part 3: Adding Messages

### add_user_message()

```python
def add_user_message(self, content: str) -> None:
    """Add a user message to history."""
    self.messages.append(HumanMessage(content=content))
    self._trim_if_needed()
```

### add_ai_message()

```python
def add_ai_message(self, content: str) -> None:
    """Add an AI message to history."""
    self.messages.append(AIMessage(content=content))
    self._trim_if_needed()
```

### add_exchange()

```python
def add_exchange(self, user_message: str, ai_message: str) -> None:
    """Add a complete exchange (user + AI messages)."""
    self.add_user_message(user_message)
    self.add_ai_message(ai_message)
```

### Message Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Adding Messages                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  add_user_message("Hello!")                                     │
│       ↓                                                          │
│  messages = [HumanMessage("Hello!")]                            │
│                                                                  │
│  add_ai_message("Hi there!")                                    │
│       ↓                                                          │
│  messages = [                                                    │
│      HumanMessage("Hello!"),                                    │
│      AIMessage("Hi there!")                                     │
│  ]                                                               │
│                                                                  │
│  add_exchange("How are you?", "I'm doing well!")               │
│       ↓                                                          │
│  messages = [                                                    │
│      HumanMessage("Hello!"),                                    │
│      AIMessage("Hi there!"),                                    │
│      HumanMessage("How are you?"),                              │
│      AIMessage("I'm doing well!")                               │
│  ]                                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 4: Retrieving Messages

### get_messages()

```python
def get_messages(self) -> List[BaseMessage]:
    """Get all messages in history."""
    return self.messages.copy()
```

### get_history_string()

```python
def get_history_string(self) -> str:
    """Get history as formatted string."""
    lines = []
    for msg in self.messages:
        if isinstance(msg, HumanMessage):
            lines.append(f"Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            lines.append(f"AI: {msg.content}")
    return "\n".join(lines)
```

### Output Formats

**As Message Objects:**
```python
[
    HumanMessage(content="What is RAG?"),
    AIMessage(content="RAG stands for Retrieval-Augmented Generation..."),
    HumanMessage(content="How does it work?"),
    AIMessage(content="It works by first retrieving relevant...")
]
```

**As String:**
```
Human: What is RAG?
AI: RAG stands for Retrieval-Augmented Generation...
Human: How does it work?
AI: It works by first retrieving relevant...
```

---

## Part 5: Memory Management

### clear()

```python
def clear(self) -> None:
    """Clear all messages from history."""
    self.messages = []
```

### _trim_if_needed()

```python
def _trim_if_needed(self) -> None:
    """Trim old messages if max_messages is set."""
    if self.max_messages is not None:
        # Keep max_messages pairs (2 messages per pair)
        max_total = self.max_messages * 2
        if len(self.messages) > max_total:
            self.messages = self.messages[-max_total:]
```

### Trimming Behavior

```
┌─────────────────────────────────────────────────────────────────┐
│                 Memory Trimming (max_messages=2)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Before trim (3 exchanges = 6 messages):                        │
│  [                                                               │
│      HumanMessage("Message 1"),   ←── Will be removed           │
│      AIMessage("Response 1"),     ←── Will be removed           │
│      HumanMessage("Message 2"),                                 │
│      AIMessage("Response 2"),                                   │
│      HumanMessage("Message 3"),                                 │
│      AIMessage("Response 3"),                                   │
│  ]                                                               │
│                                                                  │
│  After trim (max_messages=2 → keep 4 messages):                 │
│  [                                                               │
│      HumanMessage("Message 2"),                                 │
│      AIMessage("Response 2"),                                   │
│      HumanMessage("Message 3"),                                 │
│      AIMessage("Response 3"),                                   │
│  ]                                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 6: Session-Based Memory

### Global Storage

```python
# Session-based memory storage
_session_memories: Dict[str, ChatMemory] = {}
```

### get_session_memory()

```python
def get_session_memory(session_id: str, max_messages: int = 10) -> ChatMemory:
    """
    Get or create memory for a session.
    
    Args:
        session_id: Unique session identifier
        max_messages: Maximum message pairs to keep
        
    Returns:
        ChatMemory instance for the session
    """
    if session_id not in _session_memories:
        _session_memories[session_id] = ChatMemory(max_messages=max_messages)
    return _session_memories[session_id]
```

### clear_session_memory()

```python
def clear_session_memory(session_id: str) -> None:
    """Clear memory for a specific session."""
    if session_id in _session_memories:
        _session_memories[session_id].clear()
```

### clear_all_memories()

```python
def clear_all_memories() -> None:
    """Clear all session memories."""
    _session_memories.clear()
```

### Session Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Session Memory Management                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User A (session: "abc123"):                                    │
│       ↓                                                          │
│  get_session_memory("abc123")                                   │
│       ↓                                                          │
│  Creates/returns ChatMemory for "abc123"                        │
│                                                                  │
│  User B (session: "xyz789"):                                    │
│       ↓                                                          │
│  get_session_memory("xyz789")                                   │
│       ↓                                                          │
│  Creates/returns ChatMemory for "xyz789"                        │
│                                                                  │
│  _session_memories = {                                          │
│      "abc123": ChatMemory(...),                                 │
│      "xyz789": ChatMemory(...),                                 │
│  }                                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 7: Memory Trade-offs

### Window Size Considerations

| Window Size | Pros | Cons |
|-------------|------|------|
| Small (3-5) | Less token usage, faster | May lose important context |
| Medium (10) | Good balance | Moderate token usage |
| Large (20+) | Full context | High token usage, slower |

### Token Usage Impact

```
Approximate tokens per exchange:
- Short exchange: ~100 tokens
- Medium exchange: ~300 tokens
- Long exchange: ~500+ tokens

With max_messages=10 (medium exchanges):
- Memory tokens: 10 × 300 = 3,000 tokens
- Plus current query and context: ~4,000 tokens
- Total per request: ~7,000 tokens

GPT-4o-mini context: 128K tokens
→ Plenty of room for memory
```

---

## Usage Examples

### Basic Memory Usage

```python
from src.memory import ChatMemory

# Create memory with 5-exchange limit
memory = ChatMemory(max_messages=5)

# Add conversation
memory.add_user_message("What is Python?")
memory.add_ai_message("Python is a programming language...")

# Get formatted history
print(memory.get_history_string())
```

### Session-Based Usage

```python
from src.memory import get_session_memory, clear_session_memory

# Get memory for a session
session_id = "user_123_session"
memory = get_session_memory(session_id)

# Add exchanges
memory.add_exchange(
    "What is machine learning?",
    "Machine learning is..."
)

# Later, clear the session
clear_session_memory(session_id)
```

### With RAG Chain

```python
from src.memory import get_session_memory
from src.chain import query_rag

session_id = "user_abc"
memory = get_session_memory(session_id)

# User asks question
question = "What is the document about?"
result = query_rag(vectorstore, question)

# Save to memory
memory.add_exchange(question, result["answer"])

# Next question has context
question2 = "Can you elaborate on that?"
# Memory can be passed to chain for context
```

### Unlimited Memory

```python
# No limit - keep everything
memory = ChatMemory(max_messages=None)

# Add many messages...
for i in range(100):
    memory.add_exchange(f"Question {i}", f"Answer {i}")

print(f"Total messages: {len(memory.get_messages())}")  # 200
```

---

## Integration with RAG Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG Pipeline                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────┐                                   │
│  │      chain.py            │                                   │
│  │  query_rag()            │                                   │
│  └────────────┬─────────────┘                                   │
│               ↓                                                  │
│  ┌──────────────────────────┐                                   │
│  │      memory.py           │ ◄── YOU ARE HERE                  │
│  │  get_session_memory()    │                                   │
│  │  ChatMemory              │                                   │
│  └────────────┬─────────────┘                                   │
│               ↓                                                  │
│  ┌──────────────────────────┐                                   │
│  │       app.py             │                                   │
│  │  (Uses session state     │                                   │
│  │   for simple memory)     │                                   │
│  └──────────────────────────┘                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Current vs Future State

### Current Implementation

The app currently uses Streamlit's `st.session_state.messages` for chat history display, which is simpler for the UI but doesn't integrate memory into the RAG chain.

### Future Enhancement

For conversational RAG with memory context:

```python
# Enhanced prompt with memory
RAG_PROMPT_WITH_MEMORY = """
Previous conversation:
{chat_history}

Context from documents:
{context}

Question: {question}

Answer:"""
```

This would allow follow-up questions like:
- "Can you explain that more?"
- "What about the second point?"
- "How does this relate to what you said earlier?"

---

*Document Version: 1.0*  
*Created: January 11, 2026*
