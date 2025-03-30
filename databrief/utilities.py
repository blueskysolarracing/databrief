from dataclasses import fields, is_dataclass
from typing import Any, Type, get_origin, get_args
import struct


def _dump_field(value: Any, field_type: Type) -> bytes:
    if is_dataclass(field_type):
        packed_data = dump(value)
        return struct.pack('i', len(packed_data)) + packed_data
    elif get_origin(field_type) is list:
        element_type = get_args(field_type)[0]
        packed_list = struct.pack('i', len(value))
        for item in value:
            packed_list += _dump_field(item, element_type)
        return packed_list
    elif get_origin(field_type) is set:
        element_type = get_args(field_type)[0]
        packed_set = struct.pack('i', len(value))
        for item in value:
            packed_set += _dump_field(item, element_type)
        return packed_set
    elif get_origin(field_type) is tuple:
        element_types = get_args(field_type)
        packed_tuple = b""
        for item, element_type in zip(value, element_types):
            packed_tuple += _dump_field(item, element_type)
        return packed_tuple
    elif get_origin(field_type) is dict:
        key_type, value_type = get_args(field_type)
        packed_dict = struct.pack('i', len(value))
        for key, val in value.items():
            packed_dict += _dump_field(key, key_type)
            packed_dict += _dump_field(val, value_type)
        return packed_dict
    elif issubclass(field_type, int):  # type: ignore[arg-type]
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
    if is_dataclass(field_type):
        length = struct.unpack_from('i', data, offset)[0]
        offset += struct.calcsize('i')
        packed_data = data[offset:offset + length]
        offset += length
        value = load(packed_data, field_type)
    elif get_origin(field_type) is list:
        element_type = field_type.__args__[0]
        length = struct.unpack_from('i', data, offset)[0]
        offset += struct.calcsize('i')
        value = []
        for _ in range(length):
            item, offset = _load_field(data, offset, element_type)
            value.append(item)
    elif get_origin(field_type) is set:
        element_type = field_type.__args__[0]
        length = struct.unpack_from('i', data, offset)[0]
        offset += struct.calcsize('i')
        value = set()
        for _ in range(length):
            item, offset = _load_field(data, offset, element_type)
            value.add(item)
    elif get_origin(field_type) is tuple:
        element_types = get_args(field_type)
        value = []
        for element_type in element_types:
            item, offset = _load_field(data, offset, element_type)
            value.append(item)
        value = tuple(value)
    elif get_origin(field_type) is dict:
        key_type, value_type = get_args(field_type)
        length = struct.unpack_from('i', data, offset)[0]
        offset += struct.calcsize('i')
        value = {}
        for _ in range(length):
            key, offset = _load_field(data, offset, key_type)
            val, offset = _load_field(data, offset, value_type)
            value[key] = val
    elif issubclass(field_type, int):  # type: ignore[arg-type]
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
        if get_origin(field.type) in {list, set, tuple, dict}:
            packed_data.extend(_dump_field(value, field.type))
        elif issubclass(field.type, bool):  # type: ignore[arg-type]
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
        if get_origin(field.type) in {list, set, tuple, dict}:
            value, offset = _load_field(data, offset, field.type)
            field_values[field.name] = value
        elif issubclass(field.type, bool):  # type: ignore[arg-type]
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
