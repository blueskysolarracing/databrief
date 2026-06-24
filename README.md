# Databrief

`databrief` is a Python library for serializing dataclasses to bytes and deserializing bytes back to dataclasses.

## Features

- Compact serialization
- Supports the following field types:
  - Primitive types: `int`, `float`, `bool`, `str`
  - Collections: `list`, `set`, `tuple`, `dict`
  - Nested dataclasses

## Installation

```sh
pip install databrief
```

## Usage

### Dumping a Dataclass to Bytes

To serialize a dataclass instance to bytes with specific integer and floating point sizes, use the `dump` function:

```python
from databrief import dump
from dataclasses import dataclass

@dataclass
class TestData:
    a: int
    b: float
    c: bool

data = TestData(a=42, b=3.14, c=True)
serialized = dump(data, 4, 8) # int32 and fp64
print(serialized)
```

### Loading Bytes to a Dataclass

To deserialize bytes back to a dataclass instance with given integer and floating point sizes, use the `load` function:

```python
from databrief import load

deserialized = load(serialized, TestData, 4, 8) # int32 and fp64
print(deserialized)
```

## Examples

Here is a complete example:

```python
from dataclasses import dataclass
from databrief import dump, load

@dataclass
class Example:
    a: int
    b: float
    c: bool
    d: bool
    e: bool
    f: bool
    g: bool
    h: bool
    i: bool
    j: bool
    k: bool
    l: float
    m: int
    n: int
    o: bool

example = Example(1, 2.0, True, False, True, False, True, False, True, True, False, 87543653.35197087, 1351346, -46583278, True)
serialized = dump(example, 4, 8)
deserialized = load(serialized, Example, 4, 8)
print(deserialized)
```

Here is another example:

```python
from dataclasses import dataclass
from databrief import dump, load

@dataclass
class InnerData:
    x: int
    y: str

@dataclass
class OuterData:
    a: int
    b: InnerData
    c: bool

example = OuterData(a=1, b=InnerData(x=42, y="hello"), c=True)
serialized = dump(example, 4, 8)
deserialized = load(serialized, OuterData, 4, 8)
print(deserialized)
```

## Contributing

### Code Style and Static Type Checking

Run style checker.

``
flake8 ./databrief
``

Run static type checker.

``
mypy --strict databrief
``

### Unit and Documentation Testing

Run unit tests.

``
python -m unittest
``

## License

Databrief is distributed under the MIT license.
