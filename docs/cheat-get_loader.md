# Cheat Sheet: get_loader()

**Factory function** that returns the correct document loader based on file extension.

---

## Function Signature

```python
def get_loader(file_path: Union[str, Path]) -> BaseLoader
```

---

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | `str` or `Path` | Path to the document file |

---

## Returns

| Loader Class | For Extension | Output |
|--------------|---------------|--------|
| `PyPDFLoader` | `.pdf` | One `Document` per page |
| `Docx2txtLoader` | `.docx` | Single `Document` |
| `TextLoader` | `.txt` | Single `Document` |

---

## Raises

| Exception | When |
|-----------|------|
| `ValueError` | File extension not in `.pdf`, `.docx`, `.txt` |

---

## Line-by-Line Breakdown

```python
file_path = Path(file_path)
```
→ Converts string to `Path` object (cross-platform)

```python
extension = file_path.suffix.lower()
```
→ Extracts `.pdf`, `.docx`, etc. and lowercases it

```python
loaders = {".pdf": PyPDFLoader, ...}
```
→ Maps extension → loader **class** (not instance)

```python
if extension not in loaders:
```
→ Validates supported file type

```python
return loaders[extension](str(file_path))
```
→ **Instantiates** loader with file path and returns it

---

## 🔍 Deep Dive: `return loaders[extension](str(file_path))`

This single line does **3 things**:

### Step 1: `loaders[extension]` — Get the Class

```python
loaders = {
    ".pdf": PyPDFLoader,      # This is the CLASS, not an instance!
    ".docx": Docx2txtLoader,
    ".txt": TextLoader,
}

# If extension = ".pdf"
loaders[".pdf"]  # Returns: PyPDFLoader (the class itself)
```

| extension | `loaders[extension]` returns |
|-----------|------------------------------|
| `".pdf"` | `PyPDFLoader` |
| `".docx"` | `Docx2txtLoader` |
| `".txt"` | `TextLoader` |

### Step 2: `(...)(str(file_path))` — Call the Constructor

The `()` after the class **calls the class constructor** (creates an instance):

```python
# These are equivalent:
loaders[".pdf"]("report.pdf")
# Same as:
PyPDFLoader("report.pdf")
```

### Step 3: Complete Picture

```python
# If file_path = "report.pdf" and extension = ".pdf"

loaders[".pdf"]              # → PyPDFLoader (class)
PyPDFLoader("report.pdf")    # → <PyPDFLoader instance>
return <PyPDFLoader instance>
```

### Visual Diagram

```
loaders[extension](str(file_path))
   │         │            │
   │         │            └── Argument to constructor
   │         │
   │         └── Get class from dictionary
   │
   └── Call the class (instantiate it)

Example: loaders[".pdf"]("report.pdf")
         ├─────────────┤├────────────┤
               │              │
         PyPDFLoader    "report.pdf"
               │              │
               └──────┬───────┘
                      ↓
            PyPDFLoader("report.pdf")
                      ↓
            <PyPDFLoader object>
```

### Why Store Classes in Dictionary?

**Factory Pattern** - instead of long if/elif chain:

```python
# ❌ Long if/elif chain
if extension == ".pdf":
    return PyPDFLoader(file_path)
elif extension == ".docx":
    return Docx2txtLoader(file_path)
elif extension == ".txt":
    return TextLoader(file_path)

# ✅ Clean dictionary lookup
return loaders[extension](file_path)
```

It's shorter, cleaner, and easy to extend (just add to the dictionary)

---

## Usage Examples

```python
# Get PDF loader
loader = get_loader("report.pdf")
docs = loader.load()  # Returns list of Documents

# Get TXT loader
loader = get_loader(Path("notes.txt"))
docs = loader.load()

# Handle unsupported type
try:
    loader = get_loader("data.xlsx")
except ValueError as e:
    print(e)  # "Unsupported file type: .xlsx..."
```

---

## Key Concepts

| Concept | Explanation |
|---------|-------------|
| **Factory Pattern** | Creates objects without specifying exact class |
| **Dict as Switch** | `loaders[ext]` replaces if/elif chain |
| **Lazy Instantiation** | Loader created only when needed |

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ValueError` | Unsupported extension | Use `.pdf`, `.docx`, or `.txt` |
| `FileNotFoundError` | File doesn't exist | Check path before calling |
| `ModuleNotFoundError` | Missing package | `pip install pypdf docx2txt` |
