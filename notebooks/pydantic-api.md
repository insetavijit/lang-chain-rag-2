# Pydantic API Reference

A comprehensive guide to Pydantic's core APIs, organized by category with clear tables and explanations.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Core Classes](#core-classes) | BaseModel, Field, ConfigDict |
| [Validators](#validators) | field_validator, model_validator, BeforeValidator, AfterValidator |
| [Serialization](#serialization) | model_dump, model_dump_json, model_copy |
| [Deserialization](#deserialization) | model_validate, model_validate_json, model_construct |
| [Type Annotations](#type-annotations) | Optional, Union, Literal, Annotated |
| [Settings](#settings) | BaseSettings, SettingsConfigDict |
| [Error Handling](#error-handling) | ValidationError, Error methods |
| [Schema Generation](#schema-generation) | model_json_schema, model_fields |

---

## Core Classes

### BaseModel

The foundational class for all Pydantic models. Inherit from `BaseModel` to create data models with automatic validation.

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str
```

| Method/Property | Description | Return Type |
|-----------------|-------------|-------------|
| `model_dump()` | Convert model to dictionary | `dict` |
| `model_dump_json()` | Convert model to JSON string | `str` |
| `model_copy()` | Create a copy of the model | `Self` |
| `model_validate()` | Parse and validate data | `Self` |
| `model_validate_json()` | Parse JSON and validate | `Self` |
| `model_construct()` | Create without validation | `Self` |
| `model_json_schema()` | Generate JSON schema | `dict` |
| `model_fields` | Dictionary of field definitions | `dict[str, FieldInfo]` |
| `model_config` | Model configuration | `ConfigDict` |
| `model_fields_set` | Set of explicitly set fields | `set[str]` |

---

### Field

Use `Field()` to add metadata, constraints, and configuration to model fields.

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(default=0.0, ge=0)
    sku: str = Field(..., pattern=r"^[A-Z]{3}-\d{4}$")
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `default` | `Any` | Default value for the field |
| `default_factory` | `Callable` | Factory function for default value |
| `alias` | `str` | Alternative name for parsing |
| `validation_alias` | `str \| AliasPath` | Alias used only for validation |
| `serialization_alias` | `str` | Alias used only for serialization |
| `title` | `str` | Title for JSON schema |
| `description` | `str` | Description for documentation |
| `examples` | `list` | Example values |
| `exclude` | `bool` | Exclude from serialization |
| `deprecated` | `bool` | Mark field as deprecated |
| `frozen` | `bool` | Make field immutable |

#### String Constraints

| Parameter | Type | Description |
|-----------|------|-------------|
| `min_length` | `int` | Minimum string length |
| `max_length` | `int` | Maximum string length |
| `pattern` | `str` | Regex pattern to match |
| `strip_whitespace` | `bool` | Strip leading/trailing whitespace |
| `to_lower` | `bool` | Convert to lowercase |
| `to_upper` | `bool` | Convert to uppercase |

#### Numeric Constraints

| Parameter | Type | Description |
|-----------|------|-------------|
| `gt` | `float` | Greater than |
| `ge` | `float` | Greater than or equal |
| `lt` | `float` | Less than |
| `le` | `float` | Less than or equal |
| `multiple_of` | `float` | Must be multiple of value |
| `allow_inf_nan` | `bool` | Allow infinity/NaN |

---

### ConfigDict

Configure model behavior using `model_config` with `ConfigDict`.

```python
from pydantic import BaseModel, ConfigDict

class StrictModel(BaseModel):
    model_config = ConfigDict(
        strict=True,
        frozen=True,
        extra='forbid'
    )
    name: str
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `strict` | `bool` | `False` | Disable type coercion |
| `frozen` | `bool` | `False` | Make model immutable |
| `extra` | `str` | `'ignore'` | Handle extra fields: `'allow'`, `'forbid'`, `'ignore'` |
| `validate_assignment` | `bool` | `False` | Validate on attribute assignment |
| `validate_default` | `bool` | `False` | Validate default values |
| `str_strip_whitespace` | `bool` | `False` | Strip whitespace from strings |
| `str_min_length` | `int` | `None` | Minimum length for all strings |
| `str_max_length` | `int` | `None` | Maximum length for all strings |
| `str_to_lower` | `bool` | `False` | Convert all strings to lowercase |
| `str_to_upper` | `bool` | `False` | Convert all strings to uppercase |
| `populate_by_name` | `bool` | `False` | Allow field name and alias |
| `alias_generator` | `Callable` | `None` | Function to generate aliases |
| `use_enum_values` | `bool` | `False` | Use enum values instead of members |
| `arbitrary_types_allowed` | `bool` | `False` | Allow custom class types |
| `from_attributes` | `bool` | `False` | Parse from ORM objects |
| `loc_by_alias` | `bool` | `True` | Use alias in error locations |
| `revalidate_instances` | `str` | `'never'` | When to revalidate model instances |
| `ser_json_timedelta` | `str` | `'iso8601'` | Timedelta serialization format |
| `ser_json_bytes` | `str` | `'utf8'` | Bytes serialization format |
| `ser_json_inf_nan` | `str` | `'null'` | Inf/NaN serialization |
| `coerce_numbers_to_str` | `bool` | `False` | Coerce numbers to strings |
| `regex_engine` | `str` | `'rust-regex'` | Regex engine to use |

---

## Validators

### field_validator

Validate individual fields with custom logic.

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        return v.lower()
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `*fields` | `str` | Field names to validate |
| `mode` | `str` | `'before'`, `'after'`, `'wrap'`, `'plain'` |
| `check_fields` | `bool` | Verify field names exist |

#### Validation Modes

| Mode | Description |
|------|-------------|
| `'before'` | Run before Pydantic's internal validation |
| `'after'` | Run after Pydantic's internal validation (default) |
| `'wrap'` | Receive a handler to call inner validation |
| `'plain'` | Replace Pydantic's validation entirely |

---

### model_validator

Validate across multiple fields at the model level.

```python
from pydantic import BaseModel, model_validator

class Registration(BaseModel):
    password: str
    confirm_password: str
    
    @model_validator(mode='after')
    def passwords_match(self) -> 'Registration':
        if self.password != self.confirm_password:
            raise ValueError('passwords do not match')
        return self
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `mode` | `str` | `'before'`, `'after'`, `'wrap'` |

#### Model Validation Modes

| Mode | Receives | Returns | Description |
|------|----------|---------|-------------|
| `'before'` | Raw input data | `dict` | Validate/transform before field parsing |
| `'after'` | Model instance | Model | Validate after all fields parsed |
| `'wrap'` | Data + handler | Model | Control entire validation flow |

---

### Annotated Validators

Use with `Annotated` type hints for reusable validation.

```python
from pydantic import BaseModel, BeforeValidator, AfterValidator
from typing import Annotated

def strip_spaces(v: str) -> str:
    return v.strip()

def validate_not_empty(v: str) -> str:
    if not v:
        raise ValueError('cannot be empty')
    return v

CleanString = Annotated[str, BeforeValidator(strip_spaces), AfterValidator(validate_not_empty)]
```

| Validator | Description |
|-----------|-------------|
| `BeforeValidator` | Run before type conversion |
| `AfterValidator` | Run after type conversion |
| `PlainValidator` | Replace default validation |
| `WrapValidator` | Wrap default validation |

---

## Serialization

### model_dump()

Convert model to a dictionary.

```python
user.model_dump()
user.model_dump(exclude={'password'})
user.model_dump(include={'name', 'email'})
user.model_dump(by_alias=True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | `str` | `'python'` | `'python'` or `'json'` mode |
| `include` | `set` | `None` | Fields to include |
| `exclude` | `set` | `None` | Fields to exclude |
| `context` | `Any` | `None` | Context for serializers |
| `by_alias` | `bool` | `False` | Use field aliases |
| `exclude_unset` | `bool` | `False` | Exclude fields not explicitly set |
| `exclude_defaults` | `bool` | `False` | Exclude fields with default values |
| `exclude_none` | `bool` | `False` | Exclude fields with None values |
| `round_trip` | `bool` | `False` | Enable round-trip serialization |
| `warnings` | `bool \| str` | `True` | How to handle warnings |
| `serialize_as_any` | `bool` | `False` | Serialize with runtime type |

---

### model_dump_json()

Convert model directly to JSON string.

```python
user.model_dump_json()
user.model_dump_json(indent=2)
user.model_dump_json(exclude={'internal_id'})
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `indent` | `int` | `None` | JSON indentation |
| `include` | `set` | `None` | Fields to include |
| `exclude` | `set` | `None` | Fields to exclude |
| `context` | `Any` | `None` | Context for serializers |
| `by_alias` | `bool` | `False` | Use field aliases |
| `exclude_unset` | `bool` | `False` | Exclude unset fields |
| `exclude_defaults` | `bool` | `False` | Exclude default values |
| `exclude_none` | `bool` | `False` | Exclude None values |
| `round_trip` | `bool` | `False` | Round-trip mode |
| `warnings` | `bool \| str` | `True` | Warning handling |
| `serialize_as_any` | `bool` | `False` | Runtime type serialization |

---

### model_copy()

Create a copy of the model, optionally with updates.

```python
user_copy = user.model_copy()
updated_user = user.model_copy(update={'name': 'New Name'})
deep_copy = user.model_copy(deep=True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `update` | `dict` | `None` | Fields to update in copy |
| `deep` | `bool` | `False` | Deep copy nested objects |

---

## Deserialization

### model_validate()

Parse and validate data from a dictionary.

```python
user = User.model_validate({'name': 'Alice', 'age': 30})
user = User.model_validate(data, strict=True)
user = User.model_validate(orm_object, from_attributes=True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `obj` | `Any` | Required | Data to validate |
| `strict` | `bool` | `None` | Disable type coercion |
| `from_attributes` | `bool` | `None` | Parse from object attributes |
| `context` | `Any` | `None` | Validation context |

---

### model_validate_json()

Parse and validate directly from JSON string or bytes.

```python
user = User.model_validate_json('{"name": "Alice", "age": 30}')
user = User.model_validate_json(json_bytes, strict=True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `json_data` | `str \| bytes` | Required | JSON to parse |
| `strict` | `bool` | `None` | Disable type coercion |
| `context` | `Any` | `None` | Validation context |

---

### model_construct()

Create model instance without validation (use with caution).

```python
# Skip validation - faster but unsafe
user = User.model_construct(name='Alice', age=30)
user = User.model_construct(_fields_set={'name'}, name='Alice', age=30)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `_fields_set` | `set` | `None` | Fields to mark as set |
| `**values` | `Any` | - | Field values |

> ⚠️ **Warning**: `model_construct()` bypasses validation entirely. Only use when you're certain the data is already valid.

---

## Type Annotations

### Common Type Patterns

| Type | Import | Description |
|------|--------|-------------|
| `Optional[T]` | `typing` | Field can be `T` or `None` |
| `Union[A, B]` | `typing` | Field can be `A` or `B` |
| `Literal['a', 'b']` | `typing` | Field must be one of the values |
| `Annotated[T, ...]` | `typing` | Add metadata to type |
| `List[T]` | `typing` | List of type `T` |
| `Dict[K, V]` | `typing` | Dictionary with key/value types |
| `Set[T]` | `typing` | Set of type `T` |
| `Tuple[A, B]` | `typing` | Fixed-length tuple |

### Pydantic Types

```python
from pydantic import (
    PositiveInt, NegativeInt, PositiveFloat, NegativeFloat,
    StrictInt, StrictFloat, StrictStr, StrictBool,
    EmailStr, NameEmail, HttpUrl, AnyUrl,
    SecretStr, SecretBytes, FilePath, DirectoryPath,
    Json, UUID1, UUID4, conint, constr, confloat
)
```

| Type | Description |
|------|-------------|
| `PositiveInt` | Integer > 0 |
| `NegativeInt` | Integer < 0 |
| `PositiveFloat` | Float > 0 |
| `NegativeFloat` | Float < 0 |
| `StrictInt` | Integer, no coercion |
| `StrictFloat` | Float, no coercion |
| `StrictStr` | String, no coercion |
| `StrictBool` | Boolean, no coercion |
| `EmailStr` | Validated email address |
| `HttpUrl` | Validated HTTP/HTTPS URL |
| `AnyUrl` | Any validated URL |
| `SecretStr` | String hidden in repr |
| `SecretBytes` | Bytes hidden in repr |
| `FilePath` | Existing file path |
| `DirectoryPath` | Existing directory path |
| `Json[T]` | JSON string parsed to type T |
| `UUID1`, `UUID4` | UUID versions |

### Constrained Types

```python
from pydantic import conint, constr, confloat, conlist

# Constrained integer
SmallInt = conint(ge=0, le=100)

# Constrained string  
ShortStr = constr(min_length=1, max_length=50)

# Constrained float
Percentage = confloat(ge=0, le=100)

# Constrained list
ShortList = conlist(str, min_length=1, max_length=5)
```

| Function | Parameters |
|----------|------------|
| `conint()` | `gt`, `ge`, `lt`, `le`, `multiple_of`, `strict` |
| `constr()` | `min_length`, `max_length`, `pattern`, `strip_whitespace`, `to_lower`, `to_upper`, `strict` |
| `confloat()` | `gt`, `ge`, `lt`, `le`, `multiple_of`, `allow_inf_nan`, `strict` |
| `conlist()` | `item_type`, `min_length`, `max_length`, `unique_items` |
| `conset()` | `item_type`, `min_length`, `max_length` |
| `conbytes()` | `min_length`, `max_length`, `strict` |

---

## Settings

### BaseSettings

Configuration management with environment variable support.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='APP_',
        case_sensitive=False
    )
    
    debug: bool = False
    database_url: str
    api_key: str

settings = Settings()
```

| Config Option | Type | Default | Description |
|---------------|------|---------|-------------|
| `env_file` | `str \| Path` | `None` | Path to .env file |
| `env_file_encoding` | `str` | `None` | Encoding of .env file |
| `env_prefix` | `str` | `''` | Prefix for env variables |
| `env_nested_delimiter` | `str` | `None` | Delimiter for nested settings |
| `case_sensitive` | `bool` | `False` | Case-sensitive env names |
| `secrets_dir` | `str \| Path` | `None` | Directory for secret files |
| `json_file` | `str \| Path` | `None` | Path to JSON config file |
| `toml_file` | `str \| Path` | `None` | Path to TOML config file |
| `yaml_file` | `str \| Path` | `None` | Path to YAML config file |
| `extra` | `str` | `'forbid'` | Handle extra fields |

> 📦 **Note**: Install with `pip install pydantic-settings`

---

## Error Handling

### ValidationError

Raised when validation fails. Contains detailed error information.

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

try:
    User(name='Alice', age='not a number')
except ValidationError as e:
    print(e.error_count())  # Number of errors
    print(e.errors())       # List of error dicts
    print(e.json())         # Errors as JSON
```

| Method | Return Type | Description |
|--------|-------------|-------------|
| `errors()` | `list[dict]` | List of error dictionaries |
| `error_count()` | `int` | Total number of errors |
| `json()` | `str` | Errors as JSON string |

### Error Dictionary Structure

Each error in `errors()` contains:

| Key | Type | Description |
|-----|------|-------------|
| `type` | `str` | Error type identifier |
| `loc` | `tuple` | Location of error (field path) |
| `msg` | `str` | Human-readable message |
| `input` | `Any` | The invalid input value |
| `ctx` | `dict` | Additional context (optional) |
| `url` | `str` | Link to documentation |

```python
# Example error structure
{
    'type': 'int_parsing',
    'loc': ('age',),
    'msg': 'Input should be a valid integer',
    'input': 'not a number',
    'url': 'https://errors.pydantic.dev/2/v/int_parsing'
}
```

---

## Schema Generation

### model_json_schema()

Generate JSON Schema for OpenAPI/Swagger documentation.

```python
schema = User.model_json_schema()
schema = User.model_json_schema(mode='serialization')
schema = User.model_json_schema(ref_template='#/definitions/{model}')
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `by_alias` | `bool` | `True` | Use aliases in schema |
| `ref_template` | `str` | `'#/$defs/{model}'` | Template for $ref |
| `schema_generator` | `type` | `GenerateJsonSchema` | Schema generator class |
| `mode` | `str` | `'validation'` | `'validation'` or `'serialization'` |

### model_fields

Access field information programmatically.

```python
for name, field_info in User.model_fields.items():
    print(f"{name}: {field_info.annotation}")
    print(f"  Required: {field_info.is_required()}")
    print(f"  Default: {field_info.default}")
```

| FieldInfo Attribute | Type | Description |
|---------------------|------|-------------|
| `annotation` | `type` | Field type annotation |
| `default` | `Any` | Default value |
| `default_factory` | `Callable` | Default factory |
| `alias` | `str` | Field alias |
| `title` | `str` | Field title |
| `description` | `str` | Field description |
| `examples` | `list` | Example values |
| `exclude` | `bool` | Exclude from serialization |
| `deprecated` | `bool` | Deprecated flag |
| `is_required()` | Method | Check if field is required |

---

## Quick Reference

### Import Cheat Sheet

```python
# Core
from pydantic import BaseModel, Field, ConfigDict

# Validators
from pydantic import field_validator, model_validator
from pydantic import BeforeValidator, AfterValidator, PlainValidator, WrapValidator

# Errors
from pydantic import ValidationError

# Types
from pydantic import (
    PositiveInt, NegativeInt, PositiveFloat, NegativeFloat,
    StrictInt, StrictFloat, StrictStr, StrictBool,
    EmailStr, HttpUrl, AnyUrl, SecretStr,
    conint, constr, confloat, conlist
)

# Settings (separate package)
from pydantic_settings import BaseSettings, SettingsConfigDict

# Typing
from typing import Optional, Union, Literal, Annotated, List, Dict
```

### Common Patterns

| Pattern | Example |
|---------|---------|
| Required field | `name: str` |
| Optional field | `bio: Optional[str] = None` |
| Field with default | `role: str = "user"` |
| Constrained field | `age: int = Field(..., ge=0, le=150)` |
| Aliased field | `user_id: int = Field(..., alias='userId')` |
| Excluded field | `internal: str = Field(exclude=True)` |
| Validated field | `@field_validator('email')` |
| Immutable model | `model_config = ConfigDict(frozen=True)` |
| Strict mode | `model_config = ConfigDict(strict=True)` |

---

## Version Notes

This documentation is based on **Pydantic v2.x**. Key differences from v1:

| Feature | Pydantic v1 | Pydantic v2 |
|---------|-------------|-------------|
| Model export | `.dict()` | `.model_dump()` |
| JSON export | `.json()` | `.model_dump_json()` |
| Parsing | `.parse_obj()` | `.model_validate()` |
| JSON parsing | `.parse_raw()` | `.model_validate_json()` |
| Config class | `class Config:` | `model_config = ConfigDict()` |
| Validators | `@validator` | `@field_validator` |
| Root validators | `@root_validator` | `@model_validator` |
| Schema method | `.schema()` | `.model_json_schema()` |
| Copy method | `.copy()` | `.model_copy()` |

---

*Last updated: January 2026*
