"""TODO(cjdrake): Write docstring."""

from bvwx import land, lor, lxor

LOR_VALS = [
    ((), "1b0"),
    (("1b0", "1b0"), "1b0"),
    (("1b0", "1b1"), "1b1"),
    (("1b1", "1b0"), "1b1"),
    (("1b1", "1b1"), "1b1"),
    (("1b0", "1b0", "1b0"), "1b0"),
    (("1b0", "1b-"), "1b-"),
    (("1b1", "1b-"), "1b1"),
    (("1b0", "1bX"), "1bX"),
    (("1b1", "1bX"), "1bX"),
]


def test_lor():
    for xs, y in LOR_VALS:
        assert lor(*xs) == y


LAND_VALS = [
    ((), "1b1"),
    (("1b0", "1b0"), "1b0"),
    (("1b0", "1b1"), "1b0"),
    (("1b1", "1b0"), "1b0"),
    (("1b1", "1b1"), "1b1"),
    (("1b1", "1b1", "1b1"), "1b1"),
    (("1b1", "1b-"), "1b-"),
    (("1b0", "1b-"), "1b0"),
    (("1b0", "1bX"), "1bX"),
    (("1b1", "1bX"), "1bX"),
]


def test_land():
    for xs, y in LAND_VALS:
        assert land(*xs) == y


LXOR_VALS = [
    ((), "1b0"),
    (("1b0", "1b0"), "1b0"),
    (("1b0", "1b1"), "1b1"),
    (("1b1", "1b0"), "1b1"),
    (("1b1", "1b1"), "1b0"),
    (("1b0", "1b0", "1b1"), "1b1"),
    (("1b0", "1b1", "1b1"), "1b0"),
    (("1b1", "1b-"), "1b-"),
    (("1b0", "1b-"), "1b-"),
    (("1b0", "1bX"), "1bX"),
    (("1b1", "1bX"), "1bX"),
]


def test_lxor():
    for xs, y in LXOR_VALS:
        assert lxor(*xs) == y
