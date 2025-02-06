from dataclasses import fields, is_dataclass
from typing import Any, Type
import struct


def _dump_field(value: Any, field_type: Type) -> bytes:
    if issubclass(field_type, int):  # type: ignore[arg-type]
        return struct.pack('i', value)
    elif issubclass(field_type, float):  # type: ignore[arg-type]
        return struct.pack('d', value)
    elif issubclass(field_type, bool):  # type: ignore[arg-type]
        return struct.pack('?', value)
    elif issubclass(field_type, str):
        encoded_string = value.encode('utf-8')
        return struct.pack('i', len(encoded_string)) + encoded_string
    else:
        raise TypeError(f'Unsupported field type {field_type}')

def _load_field(data: bytes, offset: int, field_type: Type) -> (Any, int):
    if issubclass(field_type, int):  # type: ignore[arg-type]
        value = struct.unpack_from('i', data, offset)[0]
        offset += struct.calcsize('i')
    elif issubclass(field_type, float):  # type: ignore[arg-type]
        value = struct.unpack_from('d', data, offset)[0]
        offset += struct.calcsize('d')
    elif issubclass(field_type, bool):  # type: ignore[arg-type]
        value = struct.unpack_from('?', data, offset)[0]
        offset += struct.calcsize('?')
    elif issubclass(field_type, str):
        length = struct.unpack_from('i', data, offset)[0]
        offset += struct.calcsize('i')
        value = data[offset:offset + length].decode('utf-8')
        offset += length
    else:
        raise TypeError(f'Unsupported field type {field_type}')
    return value, offset

def dump(instance: Any) -> bytes:
    if not is_dataclass(instance):
        raise TypeError('Dump function only accepts dataclass instances.')

    packed_data = bytearray()
    bools = []

    for field in fields(instance):
        value = getattr(instance, field.name)
        if issubclass(field.type, bool):  # type: ignore[arg-type]
            bools.append(value)
        else:
            packed_data.extend(_dump_field(value, field.type))
    
    bool_bytes = bytearray()

    for i in range(0, len(bools), 8):
        bool_byte = sum(1 << j for j, b in enumerate(bools[i:i + 8]) if b)
        bool_bytes.append(bool_byte)

    return bytes(packed_data) + bytes(bool_bytes)


def load(data: bytes, cls: Type[Any]) -> Any:
    if not is_dataclass(cls):
        raise TypeError('Load function only accepts dataclass types.')

    offset = 0
    field_values = {}
    bool_fields = []

    for field in fields(cls):
        if issubclass(field.type, bool):  # type: ignore[arg-type]
            bool_fields.append(field)
        else:
            value, offset = _load_field(data, offset, field.type)
            field_values[field.name] = value

    bool_values = []
    bool_byte = 0

    for i in range(len(bool_fields)):
        if i % 8 == 0:
            bool_byte = struct.unpack_from('B', data, offset)[0]
            offset += struct.calcsize('B')

        bool_values.append((bool_byte >> (i % 8)) & 1)

    for field, value in zip(bool_fields, bool_values):
        field_values[field.name] = bool(value)

    return cls(**field_values)
