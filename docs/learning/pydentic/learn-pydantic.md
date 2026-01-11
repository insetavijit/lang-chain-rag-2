# Learn Pydantic: A Practical Guide

*Understanding Pydantic from basics to practical usage*


---

> [!TIP]
> **Interactive Version Available!**
> You can run and modify the examples in this guide using the [Jupyter Notebook](../../notebooks/learn_pydantic.ipynb).

---


## What is Pydantic?

Pydantic is a **data validation library** for Python. It uses Python type hints to:
- ✅ Validate data automatically
- ✅ Convert data to correct types
- ✅ Provide clear error messages
- ✅ Create settings from environment variables

---

## Part 1: Basic Models

### Your First Model

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    is_active: bool = True  # Default value

# Create a user
user = User(name="Alice", age=30)
print(user.name)       # "Alice"
print(user.age)        # 30
print(user.is_active)  # True (default)
```

### Automatic Type Conversion

```python
# Pydantic converts types automatically!
user = User(name="Bob", age="25")  # age as string
print(user.age)        # 25 (converted to int)
print(type(user.age))  # <class 'int'>
```

### Validation Errors

```python
try:
    user = User(name="Charlie", age="not a number")
except ValidationError as e:
    print(e)
    # age: Input should be a valid integer
```

---

## Part 2: Field Types

### Common Types

```python
from typing import Optional, List, Dict
from pydantic import BaseModel

class Config(BaseModel):
    # Required fields
    name: str
    count: int
    price: float
    enabled: bool
    
    # Optional fields (can be None)
    description: Optional[str] = None
    
    # Collections
    tags: List[str] = []
    metadata: Dict[str, str] = {}
```

### Type Validation Table

| Python Type | Valid Inputs | Converted To |
|-------------|--------------|--------------|
| `str` | "hello", 123 | "hello", "123" |
| `int` | 42, "42", 42.0 | 42, 42, 42 |
| `float` | 3.14, "3.14", 3 | 3.14, 3.14, 3.0 |
| `bool` | True, "true", 1 | True, True, True |
| `List[str]` | ["a", "b"] | ["a", "b"] |

---

## Part 3: The Field Function

### Adding Constraints

```python
from pydantic import BaseModel, Field

class Settings(BaseModel):
    # With default
    chunk_size: int = Field(default=800)
    
    # With constraints
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    
    # With description
    api_key: str = Field(description="Your API key")
```

### Field Options

| Option | Example | Purpose |
|--------|---------|---------|
| `default` | `Field(default=100)` | Default value |
| `ge` | `Field(ge=0)` | Greater than or equal |
| `le` | `Field(le=100)` | Less than or equal |
| `min_length` | `Field(min_length=1)` | Minimum string length |
| `max_length` | `Field(max_length=50)` | Maximum string length |

---

## Part 4: Pydantic Settings

### Environment Variable Loading

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )
    
    api_key: str
    debug: bool = False
```

**.env file:**
```env
API_KEY=my-secret-key
DEBUG=true
```

**Usage:**
```python
settings = Settings()
print(settings.api_key)  # "my-secret-key"
print(settings.debug)    # True
```

### How Matching Works

```
.env Variable Name     →  Python Attribute
──────────────────────────────────────────
OPENROUTER_API_KEY     →  openrouter_api_key
LLM_MODEL              →  llm_model
CHUNK_SIZE             →  chunk_size
```

**Rule**: Underscores and case are ignored when matching.

---

## Part 5: Nested Models

### Composing Models

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str

class Person(BaseModel):
    name: str
    address: Address  # Nested model

# Create with nested data
person = Person(
    name="Alice",
    address={"city": "New York", "country": "USA"}
)

print(person.address.city)  # "New York"
```

---

## Part 6: Methods in Models

### Adding Custom Methods

```python
from pydantic import BaseModel
from typing import Optional

class Settings(BaseModel):
    openrouter_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    def get_active_provider(self) -> str:
        """Custom method to detect provider."""
        if self.openrouter_api_key:
            return "openrouter"
        elif self.groq_api_key:
            return "groq"
        elif self.openai_api_key:
            return "openai"
        else:
            raise ValueError("No API key configured")

# Usage
settings = Settings(openrouter_api_key="sk-xxx")
print(settings.get_active_provider())  # "openrouter"
```

---

## Part 7: Practical Patterns

### Singleton Pattern (Your config.py)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    model: str = "gpt-4o-mini"

# Create ONE instance at module level
settings = Settings()

# Import and use anywhere
# from config import settings
```

### Optional with Default None

```python
from typing import Optional
from pydantic import Field

class Config(BaseModel):
    # These are optional - can be None
    api_key: Optional[str] = Field(default=None)
    
    # Check if set
    def has_api_key(self) -> bool:
        return self.api_key is not None
```

---

## Part 8: Your config.py Explained

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # 1. CONFIGURATION
    model_config = SettingsConfigDict(
        env_file=".env",           # Read from .env file
        env_file_encoding="utf-8", # File encoding
        case_sensitive=False,      # MY_VAR = my_var
        extra="ignore",            # Ignore unknown vars
    )
    
    # 2. FIELDS (auto-loaded from .env)
    openrouter_api_key: Optional[str] = Field(default=None)
    llm_model: str = Field(default="gpt-4o-mini")
    chunk_size: int = Field(default=800)
    
    # 3. METHODS
    def get_active_llm_provider(self) -> str:
        if self.openrouter_api_key:
            return "openrouter"
        raise ValueError("No API key")

# 4. SINGLETON INSTANCE
settings = Settings()  # Created once, used everywhere
```

---

## Quick Reference

### Imports

```python
# For regular models
from pydantic import BaseModel, Field

# For settings (env loading)
from pydantic_settings import BaseSettings, SettingsConfigDict

# For type hints
from typing import Optional, List, Dict
```

### Common Patterns

```python
# Required field
name: str

# Optional field (can be None)
name: Optional[str] = None

# Field with default
count: int = 10

# Field with validation
age: int = Field(ge=0, le=150)
```

---

## Why Use Pydantic?

| Without Pydantic | With Pydantic |
|------------------|---------------|
| Manual type checking | Automatic validation |
| `os.getenv()` everywhere | Centralized settings |
| String → int conversion | Auto type conversion |
| No IDE autocomplete | Full type hints |
| Runtime surprises | Early error detection |

---

## Resources

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

---

*Created: January 11, 2026*
