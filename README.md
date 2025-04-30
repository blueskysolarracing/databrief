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

To serialize a dataclass instance to bytes, use the `dump` function:

```python
from databrief import dump
from dataclasses import dataclass

@dataclass
class TestData:
    a: int
    b: float
    c: bool

data = TestData(a=42, b=3.14, c=True)
serialized = dump(data)
print(serialized)
```

### Loading Bytes to a Dataclass

To deserialize bytes back to a dataclass instance, use the `load` function:

```python
from databrief import load

deserialized = load(serialized, TestData)
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
serialized = dump(example)
deserialized = load(serialized, Example)
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
serialized = dump(example)
deserialized = load(serialized, OuterData)
print(deserialized)
```

## Contributing

Contributions are welcome! Please read our Contributing Guide for more information.

## License

Databrief is distributed under the MIT license.
