# Python Language Context

Non-obvious patterns and strategies for Python code review.

## False Positive Patterns

These patterns may appear as dead code but are actually used:

### Type Checking Guards
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from heavy_module import ExpensiveType  # Never imported at runtime
```
Imports inside `TYPE_CHECKING` blocks exist only for static type checkers. They are never executed.

### Protocol Classes
```python
class Serializable(Protocol):
    def serialize(self) -> bytes: ...  # Never called directly
```
Protocol methods define interfaces. Implementations exist in other classes that don't inherit from the protocol.

### Overload Stubs
```python
@overload
def process(x: int) -> int: ...  # Stub only
@overload
def process(x: str) -> str: ...  # Stub only
def process(x):  # Real implementation - no decorator
    return x
```
Functions with `@overload` are type stubs. Only the final undecorated implementation runs.

### Descriptor Protocol
```python
class CachedProperty:
    def __get__(self, obj, objtype=None):  # Called via attribute access
        ...
```
`__get__`, `__set__`, `__delete__` are invoked implicitly by attribute access, not direct calls.

### Subclass Hooks
```python
def __init_subclass__(cls, **kwargs):  # Called when class is subclassed
    register(cls)
```
Called implicitly when another class inherits. Search for subclass definitions.

## Tracing Strategies

Before flagging code as unused, check these locations:

1. **`__init__.py` re-exports**: Module-level functions may be re-exported for public API
2. **Entry points**: Check `pyproject.toml` `[project.scripts]` or `setup.py` `entry_points`
3. **String references**: Plugin systems often use `"module.function"` strings
4. **Framework registrations**: `admin.site.register()`, `app.register_blueprint()`, `@app.route`
5. **Test fixtures**: Functions decorated with `@pytest.fixture` in test files

## Import Resolution

### Lazy Imports
```python
def heavy_operation():
    import pandas as pd  # Only loaded when function called
```
Imports inside functions are intentionally deferred. The module may be unused at module level.

### Conditional Imports
```python
try:
    import ujson as json
except ImportError:
    import json
```
Fallback patterns - one import will always "fail" depending on environment.

### Star Re-exports
```python
# __init__.py
from .submodule import *  # Re-exports everything from submodule
```
Check `__all__` in submodules to understand what's actually exported.

## Metaprogramming

Code may be invoked through metaprogramming without direct references:

- **Metaclass hooks**: `__new__`, `__init__` in metaclasses run during class creation
- **`__set_name__`**: Called on descriptors when class is defined
- **Class decorators**: May register, wrap, or modify the decorated class
- **`__subclasshook__`**: Used by ABCs for isinstance/issubclass checks

## Pythonic Style Issues

Flag these anti-patterns:

| Anti-pattern | Preferred |
|--------------|-----------|
| `for i in range(len(lst))` | `for i, item in enumerate(lst)` |
| `map(lambda x: x*2, lst)` | `[x*2 for x in lst]` |
| `if key in d: d[key] else default` | `d.get(key, default)` |
| `"{}".format(x)` or `"%s" % x` | `f"{x}"` |
| `os.path.join(a, b)` | `Path(a) / b` |
| `found = False; for x in lst: if cond: found = True` | `any(cond for x in lst)` |
| `def f(items=[])` | `def f(items=None): items = items or []` |
| `file = open(...); try: ... finally: file.close()` | `with open(...) as file:` |
| Manual dict of counts | `collections.Counter` |
| Manual dict with default | `collections.defaultdict` |
| Relative import | Absolute import |
