from dataclasses import dataclass
from unittest import main, TestCase

from databrief.utilities import dump, load


@dataclass
class TestData:
    a: int
    b: float
    c: bool


@dataclass
class TestDataMoreFields:
    a: int
    b: float
    c: bool
    d: int
    e: float
    f: bool


@dataclass
class TestEmptyData:
    pass


@dataclass
class TestDataWithString:
    a: int
    b: str
    c: bool


@dataclass
class TestDataWithList:
    a: int
    b: list[int]
    c: bool


@dataclass
class TestDataWithTuple:
    a: int
    b: tuple[int, float, str]
    c: bool


@dataclass
class TestDataWithSet:
    a: int
    b: set[int]
    c: bool


@dataclass
class TestDataWithNestedList:
    a: int
    b: list[list[int]]
    c: bool


@dataclass
class TestDataWithDict:
    a: int
    b: dict[str, int]
    c: bool


@dataclass
class TestDataWithNestedDict:
    a: int
    b: dict[str, dict[str, int]]
    c: bool


@dataclass
class TestDataWithMixedTuple:
    a: int
    b: tuple[int, list[str], dict[str, float]]
    c: bool


@dataclass
class TestDataWithUnsupportedType:
    a: int
    b: complex  # Unsupported type
    c: bool


@dataclass
class InnerData:
    x: int
    y: str


@dataclass
class OuterData:
    a: int
    b: InnerData
    c: bool


class TestDatabrief(TestCase):
    def test_dump_and_load(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestData(a=42, b=3.125, c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestData, i, f)

                self.assertEqual(original, loaded)

    def test_dump_invalid_type(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                with self.assertRaises(TypeError):
                    dump('not a dataclass instance', i, f)

    def test_load_invalid_type(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                with self.assertRaises(TypeError):
                    load(b'\x00\x00\x00\x00', str, i, f)

    def test_negative_and_zero_values(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestData(a=-1, b=0.0, c=False)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestData, i, f)

                self.assertEqual(original, loaded)

    def test_large_number_of_booleans(self) -> None:

        @dataclass
        class ManyBools:
            b1: bool
            b2: bool
            b3: bool
            b4: bool
            b5: bool
            b6: bool
            b7: bool
            b8: bool
            b9: bool

        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = ManyBools(
                    b1=True,
                    b2=False,
                    b3=True,
                    b4=False,
                    b5=True,
                    b6=False,
                    b7=True,
                    b8=False,
                    b9=True,
                )
                dumped = dump(original, i, f)
                loaded = load(dumped, ManyBools, i, f)

                self.assertEqual(original, loaded)

    def test_all_supported_field_types(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataMoreFields(
                    a=1,
                    b=2.0,
                    c=True,
                    d=-1,
                    e=-2.0,
                    f=False,
                )
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataMoreFields, i, f)

                self.assertEqual(original, loaded)

    def test_empty_dataclass(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestEmptyData()
                dumped = dump(original, i, f)
                loaded = load(dumped, TestEmptyData, i, f)

                self.assertEqual(original, loaded)

    def test_string_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithString(a=1, b='hello', c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithString, i, f)

                self.assertEqual(original, loaded)

    def test_empty_string_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithString(a=1, b='', c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithString, i, f)

                self.assertEqual(original, loaded)

    def test_long_string_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                long_string = 'a' * 1000
                original = TestDataWithString(a=1, b=long_string, c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithString, i, f)

                self.assertEqual(original, loaded)

    def test_list_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithList(a=1, b=[1, 2, 3, 4, 5], c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithList, i, f)

                self.assertEqual(original, loaded)

    def test_empty_list_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithList(a=1, b=[], c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithList, i, f)

                self.assertEqual(original, loaded)

    def test_large_list_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                large_list = list(range(10000))
                original = TestDataWithList(a=1, b=large_list, c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithList, i, f)

        self.assertEqual(original, loaded)

    def test_tuple_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithTuple(
                    a=1, b=(42, 3.125, 'hello'), c=True
                )
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithTuple, i, f)

                self.assertEqual(original, loaded)

    def test_set_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithSet(a=1, b={1, 2, 3, 4, 5}, c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithSet, i, f)

                self.assertEqual(original, loaded)

    def test_empty_set_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithSet(a=1, b=set(), c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithSet, i, f)

                self.assertEqual(original, loaded)

    def test_nested_list_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithNestedList(
                    a=1, b=[[1, 2], [3, 4], [5]], c=True
                )
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithNestedList, i, f)

                self.assertEqual(original, loaded)

    def test_empty_nested_list_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithNestedList(a=1, b=[], c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithNestedList, i, f)

                self.assertEqual(original, loaded)

    def test_dict_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithDict(
                    a=1, b={'key1': 10, 'key2': 20}, c=True
                )
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithDict, i, f)

                self.assertEqual(original, loaded)

    def test_empty_dict_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithDict(a=1, b={}, c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithDict, i, f)

                self.assertEqual(original, loaded)

    def test_large_dict_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                large_dict = {f'key{i}': i for i in range(1000)}
                original = TestDataWithDict(a=1, b=large_dict, c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithDict, i, f)

                self.assertEqual(original, loaded)

    def test_nested_dict_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithNestedDict(
                    a=1,
                    b={'outer': {'inner1': 10, 'inner2': 20}},
                    c=True
                )
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithNestedDict, i, f)

                self.assertEqual(original, loaded)

    def test_empty_nested_dict_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithNestedDict(a=1, b={}, c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithNestedDict, i, f)

                self.assertEqual(original, loaded)

    def test_mixed_tuple_field(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithMixedTuple(
                    a=1,
                    b=(42, ['hello', 'world'], {'key': 3.125}),
                    c=True
                )
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithMixedTuple, i, f)

                self.assertEqual(original, loaded)

    def test_unsupported_type(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithUnsupportedType(
                    a=1, b=complex(1, 2), c=True
                )

                with self.assertRaises(TypeError):
                    dump(original, i, f)

    def test_dict_with_empty_string_key(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithDict(a=1, b={'': 42}, c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithDict, i, f)

                self.assertEqual(original, loaded)

    def test_nested_list_with_empty_sublists(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = TestDataWithNestedList(
                    a=1, b=[[1, 2], [], [3, 4]], c=True
                )
                dumped = dump(original, i, f)
                loaded = load(dumped, TestDataWithNestedList, i, f)

                self.assertEqual(original, loaded)

    def test_nested_dataclass(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = OuterData(a=1, b=InnerData(x=42, y='hello'), c=True)
                dumped = dump(original, i, f)
                loaded = load(dumped, OuterData, i, f)

                self.assertEqual(original, loaded)

    def test_empty_nested_dataclass(self) -> None:
        for i in [2, 4, 8]:
            for f in [2, 4, 8]:
                original = OuterData(a=1, b=InnerData(x=0, y=''), c=False)
                dumped = dump(original, i, f)
                loaded = load(dumped, OuterData, i, f)

                self.assertEqual(original, loaded)


if __name__ == '__main__':
    main()
