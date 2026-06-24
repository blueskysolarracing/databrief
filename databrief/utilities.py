from dataclasses import fields, is_dataclass
from struct import calcsize, pack, unpack_from
from typing import Any, cast, get_origin, get_args


def _dump_field(
        value: Any,
        field_type: type[Any],
        int_len: int,
        fp_len: int,
) -> bytes:
    assert int_len in [2, 4, 8], f'Unsupported int length: {int_len} bytes'
    assert fp_len in [2, 4, 8], f'Unsupported float length: {fp_len} bytes'
    packed_data = b''

    if is_dataclass(field_type):
        packed_data = (
            pack('i', len(dump(value, int_len, fp_len)))
            + dump(value, int_len, fp_len)
        )
    elif get_origin(field_type) is list:
        element_type = get_args(field_type)[0]
        packed_data = pack('i', len(value))

        for item in value:
            packed_data += _dump_field(item, element_type, int_len, fp_len)
    elif get_origin(field_type) is set:
        element_type = get_args(field_type)[0]
        packed_data = pack('i', len(value))

        for item in value:
            packed_data += _dump_field(item, element_type, int_len, fp_len)
    elif get_origin(field_type) is tuple:
        element_types = get_args(field_type)

        for item, element_type in zip(value, element_types):
            packed_data += _dump_field(item, element_type, int_len, fp_len)
    elif get_origin(field_type) is dict:
        key_type, value_type = get_args(field_type)
        packed_data = pack('i', len(value))

        for key, val in value.items():
            packed_data += _dump_field(key, key_type, int_len, fp_len)
            packed_data += _dump_field(val, value_type, int_len, fp_len)
    elif issubclass(field_type, bool):
        packed_data = pack('?', value)
    elif issubclass(field_type, int):
        match int_len:
            case 2:
                packed_data = pack('h', value)
            case 4:
                packed_data = pack('i', value)
            case 8:
                packed_data = pack('q', value)
    elif issubclass(field_type, float):
        match fp_len:
            case 2:
                packed_data = pack('e', value)
            case 4:
                packed_data = pack('f', value)
            case 8:
                packed_data = pack('d', value)
    elif issubclass(field_type, str):
        encoded_string = value.encode('utf-8')
        packed_data = pack('i', len(encoded_string)) + encoded_string
    else:
        raise TypeError(f'Unsupported field type {field_type}')

    return packed_data


def _load_field(
        data: bytes,
        offset: int,
        field_type: type[Any],
        int_len: int,
        fp_len: int,
) -> tuple[Any, int]:
    assert int_len in [2, 4, 8], f'Unsupported int length: {int_len} bytes'
    assert fp_len in [2, 4, 8], f'Unsupported float length: {fp_len} bytes'

    if is_dataclass(field_type):
        length = unpack_from('i', data, offset)[0]
        offset += calcsize('i')
        packed_data = data[offset:offset + length]
        offset += length
        value = load(packed_data, field_type, int_len, fp_len)
    elif get_origin(field_type) is list:
        element_type = field_type.__args__[0]
        length = unpack_from('i', data, offset)[0]
        offset += calcsize('i')
        value = []

        for _ in range(length):
            item, offset = _load_field(
                data, offset, element_type, int_len, fp_len
            )

            value.append(item)
    elif get_origin(field_type) is set:
        element_type = field_type.__args__[0]
        length = unpack_from('i', data, offset)[0]
        offset += calcsize('i')
        value = set()

        for _ in range(length):
            item, offset = _load_field(
                data, offset, element_type, int_len, fp_len
            )

            value.add(item)
    elif get_origin(field_type) is tuple:
        element_types = get_args(field_type)
        value = []

        for element_type in element_types:
            item, offset = _load_field(
                data, offset, element_type, int_len, fp_len
            )

            value.append(item)

        value = tuple(value)
    elif get_origin(field_type) is dict:
        key_type, value_type = get_args(field_type)
        length = unpack_from('i', data, offset)[0]
        offset += calcsize('i')
        value = {}

        for _ in range(length):
            key, offset = _load_field(
                data, offset, key_type, int_len, fp_len
            )
            val, offset = _load_field(
                data, offset, value_type, int_len, fp_len
            )
            value[key] = val
    elif issubclass(field_type, bool):
        value = unpack_from('?', data, offset)[0]
        offset += calcsize('?')
    elif issubclass(field_type, int):
        match int_len:
            case 2:
                value = unpack_from('h', data, offset)[0]
                offset += calcsize('h')
            case 4:
                value = unpack_from('i', data, offset)[0]
                offset += calcsize('i')
            case 8:
                value = unpack_from('q', data, offset)[0]
                offset += calcsize('q')
    elif issubclass(field_type, float):
        match fp_len:
            case 2:
                value = unpack_from('e', data, offset)[0]
                offset += calcsize('e')
            case 4:
                value = unpack_from('f', data, offset)[0]
                offset += calcsize('f')
            case 8:
                value = unpack_from('d', data, offset)[0]
                offset += calcsize('d')
    elif issubclass(field_type, str):
        length = unpack_from('i', data, offset)[0]
        offset += calcsize('i')
        value = data[offset:offset + length].decode('utf-8')
        offset += length
    else:
        raise TypeError(f'Unsupported field type {field_type}')

    return value, offset


def dump(instance: Any, int_len: int, fp_len: int) -> bytes:
    assert int_len in [2, 4, 8], f'Unsupported int length: {int_len} bytes'
    assert fp_len in [2, 4, 8], f'Unsupported float length: {fp_len} bytes'

    if not is_dataclass(instance):
        raise TypeError('Dump function only accepts dataclass instances.')

    packed_data = bytearray()
    bools = []

    for field in fields(instance):
        value = getattr(instance, field.name)
        field_type = cast(type[Any], field.type)

        if get_origin(field.type) in {list, set, tuple, dict}:
            packed_data.extend(
                _dump_field(value, field_type, int_len, fp_len)
            )
        elif issubclass(field_type, bool):
            bools.append(value)
        else:
            packed_data.extend(
                _dump_field(value, field_type, int_len, fp_len)
            )

    bool_bytes = bytearray()

    for i in range(0, len(bools), 8):
        bool_byte = sum(1 << j for j, b in enumerate(bools[i:i + 8]) if b)

        bool_bytes.append(bool_byte)

    return bytes(packed_data) + bytes(bool_bytes)


def load(data: bytes, cls: type[Any], int_len: int, fp_len: int) -> Any:
    assert int_len in [2, 4, 8], f'Unsupported int length: {int_len} bytes'
    assert fp_len in [2, 4, 8], f'Unsupported float length: {fp_len} bytes'

    if not is_dataclass(cls):
        raise TypeError('Load function only accepts dataclass types.')

    offset = 0
    field_values = {}
    bool_fields = []

    for field in fields(cls):
        field_type = cast(type[Any], field.type)

        if get_origin(field_type) in {list, set, tuple, dict}:
            value, offset = _load_field(
                data, offset, field_type, int_len, fp_len
            )
            field_values[field.name] = value
        elif issubclass(field_type, bool):
            bool_fields.append(field)
        else:
            value, offset = _load_field(
                data, offset, field_type, int_len, fp_len
            )
            field_values[field.name] = value

    bool_values = []
    bool_byte = 0

    for i in range(len(bool_fields)):
        if i % 8 == 0:
            bool_byte = unpack_from('B', data, offset)[0]
            offset += calcsize('B')

        bool_values.append((bool_byte >> (i % 8)) & 1)

    for field, value in zip(bool_fields, bool_values):
        field_values[field.name] = bool(value)

    return cls(**field_values)
