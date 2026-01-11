"""
Application configuration using Pydantic Settings.
Loads environment variables with validation and defaults.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # LLM Provider Keys (at least one required)
    openrouter_api_key: Optional[str] = Field(default=None)
    groq_api_key: Optional[str] = Field(default=None)
    openai_api_key: Optional[str] = Field(default=None)
    
    # Langfuse Tracing
    langfuse_secret_key: Optional[str] = Field(default=None)
    langfuse_public_key: Optional[str] = Field(default=None)
    langfuse_base_url: str = Field(default="https://cloud.langfuse.com")
    
    # Model Configuration
    llm_model: str = Field(default="gpt-4o-mini")
    embedding_model: str = Field(default="text-embedding-3-small")
    
    # RAG Settings
    chunk_size: int = Field(default=800)
    chunk_overlap: int = Field(default=200)
    retrieval_k: int = Field(default=4)
    
    # Paths
    data_dir: str = Field(default="data")
    vector_store_path: str = Field(default="data/vectorstore")
    
    def get_active_llm_provider(self) -> str:
        """Determine which LLM provider to use based on available keys."""
        if self.openrouter_api_key:
            return "openrouter"
        elif self.groq_api_key:
            return "groq"
        elif self.openai_api_key:
            return "openai"
        else:
            raise ValueError(
                "No LLM API key configured. "
                "Set OPENROUTER_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY."
            )
    
    def get_llm_base_url(self) -> Optional[str]:
        """Get the base URL for the active LLM provider."""
        provider = self.get_active_llm_provider()
        if provider == "openrouter":
            return "https://openrouter.ai/api/v1"
        elif provider == "groq":
            return "https://api.groq.com/openai/v1"
        return None  # OpenAI uses default
    
    def get_llm_api_key(self) -> str:
        """Get the API key for the active LLM provider."""
        provider = self.get_active_llm_provider()
        if provider == "openrouter":
            return self.openrouter_api_key
        elif provider == "groq":
            return self.groq_api_key
        return self.openai_api_key


# Singleton instance
settings = Settings()
