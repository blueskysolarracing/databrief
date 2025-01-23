from dataclasses import fields, is_dataclass
from typing import Any, Type
import struct


def dump(instance: Any) -> bytes:
    if not is_dataclass(instance):
        raise TypeError('Dump function only accepts dataclass instances.')

    int_float_values = []
    bools = []
    format_parts = []

    for field in fields(instance):
        value = getattr(instance, field.name)

        if issubclass(field.type, int):  # type: ignore[arg-type]
            int_float_values.append(value)
            format_parts.append('i')
        elif issubclass(field.type, float):  # type: ignore[arg-type]
            int_float_values.append(value)
            format_parts.append('d')
        elif issubclass(field.type, bool):  # type: ignore[arg-type]
            bools.append(value)
        else:
            raise TypeError(f'Unsupported field type {field.type}')

    format_string = ''.join(format_parts)
    packed_data = struct.pack(format_string, *int_float_values)
    bool_bytes = bytearray()

    for i in range(0, len(bools), 8):
        bool_byte = sum(1 << j for j, b in enumerate(bools[i:i + 8]) if b)
        bool_bytes.append(bool_byte)

    return packed_data + bytes(bool_bytes)


def load(data: bytes, cls: Type[Any]) -> Any:
    if not is_dataclass(cls):
        raise TypeError('Load function only accepts dataclass types.')

    offset = 0
    field_values = {}
    int_float_fields = []
    bool_fields = []
    format_parts = []

    for field in fields(cls):
        if issubclass(field.type, int):  # type: ignore[arg-type]
            int_float_fields.append(field)
            format_parts.append('i')
        elif issubclass(field.type, float):  # type: ignore[arg-type]
            int_float_fields.append(field)
            format_parts.append('d')
        elif issubclass(field.type, bool):  # type: ignore[arg-type]
            bool_fields.append(field)
        else:
            raise TypeError(f'Unsupported field type {field.type}')

    format_string = ''.join(format_parts)
    int_float_values = struct.unpack_from(format_string, data, offset)
    offset += struct.calcsize(format_string)

    for field, value in zip(int_float_fields, int_float_values):
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
