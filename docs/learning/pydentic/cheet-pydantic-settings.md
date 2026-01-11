# Pydantic Settings Cheat Sheet

*Quick reference for environment variable loading in config.py*

---

## How It Works (TL;DR)

```
.env file                     Python class                    Access
─────────────────────────────────────────────────────────────────────────
OPENROUTER_API_KEY=sk-...  →  openrouter_api_key: str  →  settings.openrouter_api_key
```

**Pydantic automatically matches environment variable names to class attributes!**

---

## The Magic Flow

```
┌──────────────────────┐
│       .env file      │
│ OPENROUTER_API_KEY=  │
│ sk-or-v1-xxx         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Settings() created   │
│ (line 79)            │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Pydantic reads .env  │
│ Matches names        │
│ (case-insensitive)   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ settings.openrouter_ │
│ api_key = "sk-or-..."│
└──────────────────────┘
```

---

## Key Configuration

```python
model_config = SettingsConfigDict(
    env_file=".env",           # Which file to read
    env_file_encoding="utf-8", # Encoding
    case_sensitive=False,      # OPENROUTER_API_KEY = openrouter_api_key
    extra="ignore",            # Ignore unknown vars
)
```

| Option | Value | Meaning |
|--------|-------|---------|
| `env_file` | ".env" | Load from .env in project root |
| `case_sensitive` | False | `MY_VAR` matches `my_var` |
| `extra` | "ignore" | Don't error on extra env vars |

---

## Naming Convention

| .env Variable | Python Attribute | Match? |
|---------------|------------------|--------|
| `OPENROUTER_API_KEY` | `openrouter_api_key` | ✅ Yes |
| `LLM_MODEL` | `llm_model` | ✅ Yes |
| `CHUNK_SIZE` | `chunk_size` | ✅ Yes |
| `ChunkSize` | `chunk_size` | ✅ Yes |
| `chunk_size` | `chunk_size` | ✅ Yes |

**Rule**: Remove underscores/capitals → must match attribute name

---

## Field Defaults

```python
# If .env doesn't have LLM_MODEL, use "gpt-4o-mini"
llm_model: str = Field(default="gpt-4o-mini")

# If .env doesn't have OPENROUTER_API_KEY, use None
openrouter_api_key: Optional[str] = Field(default=None)
```

---

## Priority Order

```
1. Environment variable (export CHUNK_SIZE=500)  ← Highest
2. .env file (CHUNK_SIZE=800)
3. Field default (default=800)                   ← Lowest
```

---

## Quick Examples

### Reading a Value
```python
from src.config import settings

print(settings.openrouter_api_key)  # "sk-or-v1-xxx" from .env
print(settings.chunk_size)          # 800 (from .env or default)
```

### Checking If Set
```python
if settings.openrouter_api_key:
    print("OpenRouter configured!")
else:
    print("No API key set")
```

---

## Without Pydantic (Old Way)

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Manual load

api_key = os.getenv("OPENROUTER_API_KEY")  # Manual get
chunk_size = int(os.getenv("CHUNK_SIZE", "800"))  # Manual conversion
```

## With Pydantic (New Way)

```python
from src.config import settings

api_key = settings.openrouter_api_key  # Auto-loaded
chunk_size = settings.chunk_size       # Auto-converted to int
```

**Benefits**: Type validation, defaults, no manual parsing!

---

*Created: January 11, 2026*
