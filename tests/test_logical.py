"""TODO(cjdrake): Write docstring."""

import pytest

from bvwx import bits, land, lor, lxor

T = bits(True)
F = bits(False)


LOR_VALS = [
    ((), "1b0"),
    (("1b0", "1b0"), "1b0"),
    ((False, "1b0"), "1b0"),
    ((F, "1b0"), "1b0"),
    (("1b0", False), "1b0"),
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

    with pytest.raises(TypeError):
        lor("32hdead_beef")


LAND_VALS = [
    ((), "1b1"),
    (("1b0", "1b0"), "1b0"),
    (("1b0", "1b1"), "1b0"),
    (("1b1", "1b0"), "1b0"),
    (("1b1", "1b1"), "1b1"),
    ((True, "1b1"), "1b1"),
    ((T, "1b1"), "1b1"),
    (("1b1", True), "1b1"),
    (("1b1", "1b1", "1b1"), "1b1"),
    (("1b1", "1b-"), "1b-"),
    (("1b0", "1b-"), "1b0"),
    (("1b0", "1bX"), "1bX"),
    (("1b1", "1bX"), "1bX"),
]


def test_land():
    for xs, y in LAND_VALS:
        assert land(*xs) == y

    with pytest.raises(TypeError):
        land("32hdead_beef")


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

    with pytest.raises(TypeError):
        lxor("32hdead_beef")
