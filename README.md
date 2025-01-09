# Databrief

`databrief` is a Python library for serializing dataclasses to bytes and deserializing bytes back to dataclasses.

## Features

- Compact serialization
- Supports `int`, `float`, and `bool` field types

## Installation

```sh
pip install databrief
````

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

## Example

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

## Contributing

Contributions are welcome! Please read our Contributing Guide for more information.

## License

Databrief is distributed under the MIT license.
