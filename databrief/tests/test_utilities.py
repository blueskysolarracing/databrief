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


class TestDatabrief(TestCase):
    def test_dump_and_load(self) -> None:
        original = TestData(a=42, b=3.14, c=True)
        dumped = dump(original)
        loaded = load(dumped, TestData)

        self.assertEqual(original, loaded)

    def test_dump_invalid_type(self) -> None:
        with self.assertRaises(TypeError):
            dump("not a dataclass instance")

    def test_load_invalid_type(self) -> None:
        with self.assertRaises(TypeError):
            load(b'\x00\x00\x00\x00', str)

    def test_negative_and_zero_values(self) -> None:
        original = TestData(a=-1, b=0.0, c=False)
        dumped = dump(original)
        loaded = load(dumped, TestData)

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
        dumped = dump(original)
        loaded = load(dumped, ManyBools)

        self.assertEqual(original, loaded)

    def test_all_supported_field_types(self) -> None:
        original = TestDataMoreFields(
            a=1,
            b=2.0,
            c=True,
            d=-1,
            e=-2.0,
            f=False,
        )
        dumped = dump(original)
        loaded = load(dumped, TestDataMoreFields)

        self.assertEqual(original, loaded)

    def test_empty_dataclass(self) -> None:
        original = TestEmptyData()
        dumped = dump(original)
        loaded = load(dumped, TestEmptyData)

        self.assertEqual(original, loaded)


if __name__ == '__main__':
    main()
