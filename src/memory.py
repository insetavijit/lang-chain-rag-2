"""
Conversation memory for multi-turn dialogues.
Maintains chat history for context-aware responses.
"""

from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage


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
    
    def add_user_message(self, content: str) -> None:
        """Add a user message to history."""
        self.messages.append(HumanMessage(content=content))
        self._trim_if_needed()
    
    def add_ai_message(self, content: str) -> None:
        """Add an AI message to history."""
        self.messages.append(AIMessage(content=content))
        self._trim_if_needed()
    
    def add_exchange(self, user_message: str, ai_message: str) -> None:
        """Add a complete exchange (user + AI messages)."""
        self.add_user_message(user_message)
        self.add_ai_message(ai_message)
    
    def get_messages(self) -> List[BaseMessage]:
        """Get all messages in history."""
        return self.messages.copy()
    
    def get_history_string(self) -> str:
        """Get history as formatted string."""
        lines = []
        for msg in self.messages:
            if isinstance(msg, HumanMessage):
                lines.append(f"Human: {msg.content}")
            elif isinstance(msg, AIMessage):
                lines.append(f"AI: {msg.content}")
        return "\n".join(lines)
    
    def clear(self) -> None:
        """Clear all messages from history."""
        self.messages = []
    
    def _trim_if_needed(self) -> None:
        """Trim old messages if max_messages is set."""
        if self.max_messages is not None:
            # Keep max_messages pairs (2 messages per pair)
            max_total = self.max_messages * 2
            if len(self.messages) > max_total:
                self.messages = self.messages[-max_total:]


# Session-based memory storage
_session_memories: Dict[str, ChatMemory] = {}


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


def clear_session_memory(session_id: str) -> None:
    """Clear memory for a specific session."""
    if session_id in _session_memories:
        _session_memories[session_id].clear()


def clear_all_memories() -> None:
    """Clear all session memories."""
    _session_memories.clear()
