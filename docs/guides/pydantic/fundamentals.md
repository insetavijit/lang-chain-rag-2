# Pydantic - Comprehensive Exploration Guide

| Topic | Brief |
|-------|-------|
| Basic Models | Define data structures with type hints and automatic validation |
| Field Types & Constraints | Control field behavior with validators, defaults, and constraints |
| Nested Models | Compose complex structures by embedding models within models |
| Validators | Custom validation logic using field and model validators |
| Model Configuration | Customize model behavior through Config class or model_config |
| Serialization | Convert models to dict, JSON, and control output format |
| Deserialization & Parsing | Parse raw data from dicts, JSON, and other sources |
| Aliases | Map external field names to internal Python attributes |
| Optional & Default Values | Handle missing data with Optional types and defaults |
| Union Types & Discriminators | Support multiple types for a single field |
| Generic Models | Create reusable model templates with type parameters |
| Settings Management | Load configuration from environment variables |
| Custom Types | Define your own types with custom validation |
| Error Handling | Work with validation errors and custom error messages |
| Integration with FastAPI | Use Pydantic models for request/response validation |

---

## Basic Models

Pydantic models are Python classes that inherit from `BaseModel`. They use type hints to define the structure of your data, and Pydantic automatically validates incoming data against these types. When you create an instance of a model, Pydantic checks that all required fields are present and that their values match the declared types. If validation fails, it raises a detailed error. This is the foundation of everything in Pydantic - you define what your data should look like, and Pydantic ensures it matches.

```python
from pydantic import BaseModel

# Define a simple model with typed fields
class User(BaseModel):
    name: str
    age: int
    email: str

# Create an instance - Pydantic validates the data
user = User(name="Alice", age=30, email="alice@example.com")
print(user.name)  # Alice
print(user.age)   # 30

# Pydantic converts compatible types automatically
user2 = User(name="Bob", age="25", email="bob@example.com")  # "25" -> 25
print(user2.age)  # 25 (converted to int)

# Invalid data raises ValidationError
try:
    bad_user = User(name="Charlie", age="not a number", email="test@test.com")
except Exception as e:
    print(e)  # validation error for age field
```

---

## Field Types & Constraints

Pydantic's `Field` function lets you add metadata and constraints to your model fields. You can set default values, mark fields as required, add descriptions for documentation, and apply validation constraints like minimum/maximum values or string patterns. This gives you fine-grained control over what data is acceptable without writing custom validation code. Constraints are checked automatically during model instantiation.

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    # Required field with description
    name: str = Field(..., description="Product name", min_length=1, max_length=100)
    
    # Field with default value and constraints
    price: float = Field(default=0.0, ge=0, description="Price must be non-negative")
    
    # Integer with min/max range
    quantity: int = Field(default=1, ge=1, le=1000)
    
    # String with regex pattern
    sku: str = Field(..., pattern=r"^[A-Z]{3}-\d{4}$")

# Valid product
product = Product(name="Laptop", price=999.99, quantity=10, sku="LAP-1234")
print(product)

# This fails - price is negative
try:
    bad_product = Product(name="Test", price=-10, sku="ABC-1234")
except Exception as e:
    print(e)  # price must be >= 0

# This fails - sku doesn't match pattern
try:
    bad_sku = Product(name="Test", sku="invalid")
except Exception as e:
    print(e)  # string does not match regex
```

---

## Nested Models

Real-world data is often hierarchical - an order contains items, a user has an address, a company has employees. Pydantic handles this naturally by letting you use one model as a field type in another. When you create the outer model, Pydantic recursively validates all nested structures. This keeps your code organized and ensures deep validation throughout your data hierarchy.

```python
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class Company(BaseModel):
    name: str
    address: Address  # Nested model

class Employee(BaseModel):
    name: str
    email: str
    company: Company  # Deeply nested
    skills: List[str]  # List of strings

# Create nested structure - all levels are validated
employee = Employee(
    name="Alice",
    email="alice@corp.com",
    company={
        "name": "TechCorp",
        "address": {
            "street": "123 Main St",
            "city": "San Francisco",
            "country": "USA",
            "zip_code": "94102"
        }
    },
    skills=["Python", "Pydantic", "FastAPI"]
)

print(employee.company.name)  # TechCorp
print(employee.company.address.city)  # San Francisco
```

---

## Validators

Sometimes built-in constraints aren't enough - you need custom logic to validate your data. Pydantic provides `field_validator` for validating individual fields and `model_validator` for validation that involves multiple fields. Validators run automatically during model creation and can transform data, enforce business rules, or check complex conditions that can't be expressed with simple constraints.

```python
from pydantic import BaseModel, field_validator, model_validator

class Registration(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    age: int

    # Validate a single field - runs after type conversion
    @field_validator('username')
    @classmethod
    def username_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('username must be alphanumeric')
        return v.lower()  # Transform to lowercase

    @field_validator('email')
    @classmethod
    def email_must_contain_at(cls, v):
        if '@' not in v:
            raise ValueError('invalid email format')
        return v

    # Validate across multiple fields - runs after all field validators
    @model_validator(mode='after')
    def passwords_must_match(self):
        if self.password != self.confirm_password:
            raise ValueError('passwords do not match')
        return self

# Valid registration
reg = Registration(
    username="JohnDoe123",
    email="john@example.com",
    password="secret123",
    confirm_password="secret123",
    age=25
)
print(reg.username)  # johndoe123 (lowercased by validator)

# This fails - passwords don't match
try:
    bad_reg = Registration(
        username="Jane",
        email="jane@test.com",
        password="pass1",
        confirm_password="pass2",
        age=30
    )
except Exception as e:
    print(e)  # passwords do not match
```

---

## Model Configuration

Model behavior can be customized through configuration. In Pydantic v2, you use `model_config` with a `ConfigDict` to control things like whether extra fields are allowed, if the model should be immutable, how validation errors are handled, and more. This lets you tailor Pydantic's behavior to your specific needs without changing your field definitions.

```python
from pydantic import BaseModel, ConfigDict

class StrictUser(BaseModel):
    # Configuration for this model
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Strip whitespace from strings
        str_min_length=1,           # All strings must have at least 1 char
        frozen=True,                # Make instances immutable
        extra='forbid',             # Don't allow extra fields
        validate_assignment=True,   # Validate on attribute assignment
    )
    
    name: str
    email: str

# Whitespace is stripped automatically
user = StrictUser(name="  Alice  ", email="alice@test.com")
print(repr(user.name))  # 'Alice' (stripped)

# Extra fields are forbidden
try:
    bad = StrictUser(name="Bob", email="bob@test.com", extra_field="not allowed")
except Exception as e:
    print(e)  # extra fields not permitted

# Frozen model - can't modify after creation
try:
    user.name = "Charlie"
except Exception as e:
    print(e)  # instance is frozen
```

---

## Serialization

Once you have validated data in a Pydantic model, you often need to convert it back to simple Python types or JSON for storage, API responses, or passing to other systems. Pydantic provides `model_dump()` for dictionary output and `model_dump_json()` for JSON strings. You can control which fields are included, exclude certain values, and customize the output format.

```python
from pydantic import BaseModel, Field
from datetime import datetime

class Article(BaseModel):
    title: str
    content: str
    author: str
    created_at: datetime = Field(default_factory=datetime.now)
    views: int = 0
    internal_id: str = Field(default="abc123", exclude=True)  # Excluded from output

article = Article(
    title="Pydantic Guide",
    content="Learn Pydantic step by step...",
    author="Alice"
)

# Convert to dictionary
data = article.model_dump()
print(data)
# {'title': 'Pydantic Guide', 'content': '...', 'author': 'Alice', 'created_at': ..., 'views': 0}
# Note: internal_id is excluded

# Convert to JSON string
json_str = article.model_dump_json(indent=2)
print(json_str)

# Exclude specific fields
minimal = article.model_dump(exclude={'content', 'views'})
print(minimal)  # {'title': 'Pydantic Guide', 'author': 'Alice', 'created_at': ...}

# Include only specific fields
only_title = article.model_dump(include={'title', 'author'})
print(only_title)  # {'title': 'Pydantic Guide', 'author': 'Alice'}
```

---

## Deserialization & Parsing

Pydantic can create model instances from various sources - dictionaries, JSON strings, or other objects. The `model_validate()` method parses and validates a dictionary, while `model_validate_json()` handles JSON strings directly. This is essential for processing API requests, reading configuration files, or loading data from databases.

```python
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    order_id: str
    items: List[Item]
    total: float

# Parse from dictionary
order_dict = {
    "order_id": "ORD-001",
    "items": [
        {"name": "Book", "price": 12.99},
        {"name": "Pen", "price": 1.50}
    ],
    "total": 14.49
}

order = Order.model_validate(order_dict)
print(order.order_id)  # ORD-001
print(order.items[0].name)  # Book

# Parse from JSON string
json_data = '''
{
    "order_id": "ORD-002",
    "items": [{"name": "Notebook", "price": 5.00}],
    "total": 5.00
}
'''

order2 = Order.model_validate_json(json_data)
print(order2.order_id)  # ORD-002

# Parse with strict mode - no type coercion
try:
    strict_order = Order.model_validate(
        {"order_id": 123, "items": [], "total": 0},  # order_id should be string
        strict=True
    )
except Exception as e:
    print(e)  # order_id must be a string
```

---

## Aliases

Sometimes the field names in your external data don't match what you want to use in Python. APIs might use camelCase while you prefer snake_case, or legacy systems might have cryptic field names. Aliases let you map external names to clean Python attribute names. You can also use `alias_generator` to apply transformations automatically.

```python
from pydantic import BaseModel, Field, ConfigDict

def to_camel(string: str) -> str:
    """Convert snake_case to camelCase"""
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

class ApiResponse(BaseModel):
    # Explicit alias for a single field
    user_id: int = Field(..., alias='userId')
    display_name: str = Field(..., alias='displayName')
    email_address: str = Field(..., alias='emailAddress')
    is_active: bool = Field(..., alias='isActive')

# Parse data with camelCase keys
api_data = {
    "userId": 42,
    "displayName": "Alice Smith",
    "emailAddress": "alice@example.com",
    "isActive": True
}

user = ApiResponse.model_validate(api_data)
print(user.user_id)  # 42 - access with Python name
print(user.display_name)  # Alice Smith

# Serialize back to aliases for API response
print(user.model_dump(by_alias=True))
# {'userId': 42, 'displayName': 'Alice Smith', 'emailAddress': '...', 'isActive': True}

# Using alias_generator for automatic conversion
class AutoAliasModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True  # Allow both alias and field name
    )
    
    first_name: str
    last_name: str
    created_at: str

data = {"firstName": "Bob", "lastName": "Jones", "createdAt": "2024-01-01"}
person = AutoAliasModel.model_validate(data)
print(person.first_name)  # Bob
```

---

## Optional & Default Values

Not all fields are always required. Pydantic supports optional fields using `Optional` type hint and default values. A field with a default doesn't need to be provided when creating a model. `Optional[T]` means the field can be `None`. Understanding the difference between "not provided" and "explicitly None" is important for building flexible APIs.

```python
from pydantic import BaseModel, Field
from typing import Optional

class UserProfile(BaseModel):
    # Required - must be provided
    username: str
    
    # Optional with None as default - can be omitted or set to None
    bio: Optional[str] = None
    
    # Has a default value - can be omitted
    role: str = "user"
    
    # Optional with non-None default
    notification_email: Optional[str] = Field(default=None)
    
    # Default factory for mutable defaults (important!)
    tags: list = Field(default_factory=list)

# Minimal creation - only required field
user1 = UserProfile(username="alice")
print(user1.bio)   # None
print(user1.role)  # user
print(user1.tags)  # []

# Full creation
user2 = UserProfile(
    username="bob",
    bio="Python developer",
    role="admin",
    tags=["python", "pydantic"]
)
print(user2.bio)  # Python developer

# Explicitly set to None
user3 = UserProfile(username="charlie", bio=None)
print(user3.bio)  # None
```

---

## Union Types & Discriminators

Sometimes a field can accept multiple different types - an ID might be a string or integer, a response might be a success or error object. Pydantic handles this with Union types. For complex unions of models, discriminators help Pydantic quickly determine which model to use based on a specific field value, improving both performance and error messages.

```python
from pydantic import BaseModel, Field
from typing import Union, Literal

# Simple union - field accepts multiple types
class FlexibleId(BaseModel):
    id: Union[int, str]  # Can be either int or string

print(FlexibleId(id=123))      # id=123
print(FlexibleId(id="abc"))    # id='abc'

# Discriminated union - use a field to determine type
class Cat(BaseModel):
    pet_type: Literal['cat']
    meows: int

class Dog(BaseModel):
    pet_type: Literal['dog']
    barks: int

class Fish(BaseModel):
    pet_type: Literal['fish']
    swims: bool

class Owner(BaseModel):
    name: str
    # Discriminator tells Pydantic to check 'pet_type' first
    pet: Union[Cat, Dog, Fish] = Field(..., discriminator='pet_type')

# Pydantic knows to use Cat model because pet_type='cat'
owner1 = Owner(name="Alice", pet={"pet_type": "cat", "meows": 5})
print(owner1.pet)  # pet_type='cat' meows=5
print(type(owner1.pet))  # <class 'Cat'>

# Uses Dog model
owner2 = Owner(name="Bob", pet={"pet_type": "dog", "barks": 10})
print(type(owner2.pet))  # <class 'Dog'>

# Invalid discriminator value
try:
    Owner(name="Test", pet={"pet_type": "bird", "flies": True})
except Exception as e:
    print(e)  # invalid discriminator value
```

---

## Generic Models

When you need reusable model patterns that work with different types, generics let you create templates. A paginated response wrapper, a result container, or a cache entry can be defined once and reused with any data type. Pydantic fully supports Python generics, so your type hints remain accurate and validation works correctly.

```python
from pydantic import BaseModel
from typing import TypeVar, Generic, List, Optional

# Define a type variable
T = TypeVar('T')

# Generic paginated response
class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    has_next: bool

class User(BaseModel):
    id: int
    name: str

class Product(BaseModel):
    id: int
    name: str
    price: float

# Use with User type
user_response = PaginatedResponse[User](
    items=[
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ],
    total=50,
    page=1,
    per_page=2,
    has_next=True
)
print(user_response.items[0].name)  # Alice

# Use with Product type
product_response = PaginatedResponse[Product](
    items=[{"id": 1, "name": "Laptop", "price": 999.99}],
    total=100,
    page=1,
    per_page=1,
    has_next=True
)
print(product_response.items[0].price)  # 999.99

# Generic result wrapper with error handling
class Result(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

success_result = Result[User](success=True, data={"id": 1, "name": "Alice"})
error_result = Result[User](success=False, error="User not found")
```

---

## Settings Management

Pydantic's `BaseSettings` class (from `pydantic-settings` package) is designed for configuration management. It automatically reads values from environment variables, `.env` files, and other sources. This is perfect for managing API keys, database URLs, and other configuration that shouldn't be hardcoded. Values are validated and typed just like regular models.

```python
# Install: pip install pydantic-settings
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',           # Load from .env file
        env_file_encoding='utf-8',
        extra='ignore'             # Ignore extra env vars
    )
    
    # Environment variables (case-insensitive by default)
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str = Field(..., alias='DATABASE_URL')
    api_key: str = Field(..., alias='API_KEY')
    max_connections: int = 10
    allowed_hosts: list = ["localhost"]

# Assuming these environment variables are set:
# DATABASE_URL=postgresql://localhost/mydb
# API_KEY=secret123
# DEBUG=true

settings = Settings()
print(settings.app_name)      # MyApp (default)
print(settings.debug)         # True (from env)
print(settings.database_url)  # postgresql://localhost/mydb

# Settings are validated
# If DATABASE_URL is missing and no default, raises error

# You can also load from specific .env file
# settings = Settings(_env_file='production.env')
```

---

## Custom Types

When built-in types and validators aren't enough, you can create custom types with their own validation logic. Pydantic supports this through `Annotated` types with custom validators, or by creating classes with `__get_pydantic_core_schema__`. Custom types are reusable across models and keep your validation DRY.

```python
from pydantic import BaseModel, BeforeValidator, AfterValidator, ValidationError
from typing import Annotated

# Custom type using Annotated with validators
def validate_phone(v: str) -> str:
    """Strip non-digits and validate length"""
    digits = ''.join(c for c in v if c.isdigit())
    if len(digits) != 10:
        raise ValueError('phone must have 10 digits')
    return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

def validate_positive(v: float) -> float:
    if v <= 0:
        raise ValueError('must be positive')
    return v

# Create reusable custom types
PhoneNumber = Annotated[str, AfterValidator(validate_phone)]
PositiveFloat = Annotated[float, AfterValidator(validate_positive)]

class Contact(BaseModel):
    name: str
    phone: PhoneNumber
    balance: PositiveFloat

# Phone number is validated and formatted
contact = Contact(name="Alice", phone="555-123-4567", balance=100.50)
print(contact.phone)  # (555) 123-4567

# Also works with different formats
contact2 = Contact(name="Bob", phone="(555) 987 6543", balance=50.0)
print(contact2.phone)  # (555) 987-6543

# Invalid phone
try:
    Contact(name="Test", phone="123", balance=10.0)
except ValidationError as e:
    print(e)  # phone must have 10 digits

# Invalid balance
try:
    Contact(name="Test", phone="5551234567", balance=-10.0)
except ValidationError as e:
    print(e)  # must be positive
```

---

## Error Handling

When validation fails, Pydantic raises `ValidationError` with detailed information about what went wrong. You can access the list of errors, format them for users, or convert to different formats. Understanding error structure helps you provide better feedback in APIs and user interfaces.

```python
from pydantic import BaseModel, ValidationError, Field

class CreateUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str
    age: int = Field(..., ge=18, le=120)
    password: str = Field(..., min_length=8)

# Intentionally bad data to see error handling
try:
    user = CreateUser(
        username="ab",           # Too short
        email="not-an-email",    # We'll pretend this fails
        age=15,                  # Under 18
        password="short"         # Too short
    )
except ValidationError as e:
    # Get error count
    print(f"Found {e.error_count()} errors\n")
    
    # Iterate through errors
    for error in e.errors():
        print(f"Field: {error['loc']}")
        print(f"Message: {error['msg']}")
        print(f"Type: {error['type']}")
        print()
    
    # Get as JSON for API responses
    print("JSON format:")
    print(e.json(indent=2))
    
    # Get as dict
    errors_dict = e.errors()

# Output shows:
# Field: ('username',)
# Message: String should have at least 3 characters
# Type: string_too_short
#
# Field: ('age',)
# Message: Input should be greater than or equal to 18
# Type: greater_than_equal
# etc.
```

---

## Integration with FastAPI

FastAPI is built on top of Pydantic - they work together seamlessly. Your Pydantic models automatically become request body validators, response schemas, and OpenAPI documentation. This integration means you define your data once and get validation, serialization, and docs for free.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

app = FastAPI()

# Request/Response models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # Pydantic's email validation
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]

class UsersListResponse(BaseModel):
    users: List[UserResponse]
    total: int

# Fake database
fake_db = {}
user_counter = 0

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """
    Pydantic validates the request body automatically.
    Invalid data returns 422 with detailed errors.
    """
    global user_counter
    user_counter += 1
    
    db_user = {
        "id": user_counter,
        **user.model_dump()  # Convert Pydantic model to dict
    }
    fake_db[user_counter] = db_user
    
    return db_user  # FastAPI uses UserResponse to serialize

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]

@app.get("/users", response_model=UsersListResponse)
async def list_users():
    return {
        "users": list(fake_db.values()),
        "total": len(fake_db)
    }

# To run: uvicorn filename:app --reload
# Docs available at: http://localhost:8000/docs
```
