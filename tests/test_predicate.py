"""Test bvwx predicate operators."""

import pytest

from bvwx import bits, eq, ge, gt, le, lt, match, ne, sge, sgt, sle, slt

F = bits(False)
T = bits(True)
W = bits("1b-")
X = bits("1bX")


EQ = [
    ("1b0", "1b0", T),
    ("1b0", "1b1", F),
    ("1b0", "1bX", X),
    ("1b0", "1b-", W),
    ("2b00", "2b00", T),
    ("2b00", "2b01", F),
    ("2b00", "2b0X", X),
    ("2b00", "2b0-", W),
    ("2b10", "2b10", T),
    ("2b10", "2b11", F),
    ("2b10", "2b1X", X),
    ("2b10", "2b1-", W),
]


def test_eq():
    for a, b, y in EQ:
        assert eq(bits(a), b) == y
        assert eq(a, bits(b)) == y

    # Invalid rhs
    with pytest.raises(TypeError):
        eq("1b0", "2b00")


NE = [
    ("1b0", "1b0", F),
    ("1b0", "1b1", T),
    ("1b0", "1bX", X),
    ("1b0", "1b-", W),
    ("2b00", "2b00", F),
    ("2b00", "2b01", T),
    ("2b00", "2b0X", X),
    ("2b00", "2b0-", W),
    ("2b10", "2b10", F),
    ("2b10", "2b11", T),
    ("2b10", "2b1X", X),
    ("2b10", "2b1-", W),
]


def test_ne():
    for a, b, y in NE:
        assert ne(bits(a), b) == y
        assert ne(a, bits(b)) == y

    # Invalid rhs
    with pytest.raises(TypeError):
        ne("1b0", "2b00")


LT = [
    ("1b0", "1b0", F),
    ("1b0", "1b1", T),
    ("1b1", "1b0", F),
    ("1b1", "1b1", F),
    ("1b0", "1bX", X),
    ("1b0", "1b-", W),
]


def test_lt():
    for a, b, y in LT:
        assert lt(bits(a), b) == y
        assert lt(a, bits(b)) == y

    # Invalid rhs
    with pytest.raises(TypeError):
        lt("1b0", "2b00")


LE = [
    ("1b0", "1b0", T),
    ("1b0", "1b1", T),
    ("1b1", "1b0", F),
    ("1b1", "1b1", T),
    ("1b0", "1bX", X),
    ("1b0", "1b-", W),
]


def test_le():
    for a, b, y in LE:
        assert le(bits(a), b) == y
        assert le(a, bits(b)) == y

    # Invalid rhs
    with pytest.raises(TypeError):
        le("1b0", "2b00")


SLT = [
    ("1b0", "1b0", F),
    ("1b0", "1b1", F),
    ("1b1", "1b0", T),
    ("1b1", "1b1", F),
    ("1b0", "1bX", X),
    ("1b0", "1b-", W),
]


def test_slt():
    for a, b, y in SLT:
        assert slt(bits(a), b) == y
        assert slt(a, bits(b)) == y

    # Invalid rhs
    with pytest.raises(TypeError):
        slt("1b0", "2b00")


SLE = [
    ("1b0", "1b0", T),
    ("1b0", "1b1", F),
    ("1b1", "1b0", T),
    ("1b1", "1b1", T),
    ("1b0", "1bX", X),
    ("1b0", "1b-", W),
]


def test_sle():
    for a, b, y in SLE:
        assert sle(bits(a), b) == y
        assert sle(a, bits(b)) == y

    # Invalid rhs
    with pytest.raises(TypeError):
        sle("1b0", "2b00")


GT = [
    ("1b0", "1b0", F),
    ("1b0", "1b1", F),
    ("1b1", "1b0", T),
    ("1b1", "1b1", F),
    ("1b0", "1bX", X),
    ("1b0", "1b-", W),
]


def test_gt():
    for a, b, y in GT:
        assert gt(bits(a), b) == y
        assert gt(a, bits(b)) == y

    # Invalid rhs
    with pytest.raises(TypeError):
        gt("1b0", "2b00")


GE = [
    ("1b0", "1b0", T),
    ("1b0", "1b1", F),
    ("1b1", "1b0", T),
    ("1b1", "1b1", T),
    ("1b0", "1bX", X),
    ("1b0", "1b-", W),
]


def test_ge():
    for a, b, y in GE:
        assert ge(bits(a), b) == y
        assert ge(a, bits(b)) == y

    # Invalid rhs
    with pytest.raises(TypeError):
        ge("1b0", "2b00")


SGT = [
    ("1b0", "1b0", F),
    ("1b0", "1b1", T),
    ("1b1", "1b0", F),
    ("1b1", "1b1", F),
    ("1b0", "1bX", X),
    ("1b0", "1b-", W),
]


def test_sgt():
    for a, b, y in SGT:
        assert sgt(bits(a), b) == y
        assert sgt(a, bits(b)) == y

    # Invalid rhs
    with pytest.raises(TypeError):
        sgt("1b0", "2b00")


SGE = [
    ("1b0", "1b0", T),
    ("1b0", "1b1", T),
    ("1b1", "1b0", F),
    ("1b1", "1b1", T),
    ("1b0", "1bX", X),
    ("1b0", "1b-", W),
]


def test_sge():
    for a, b, y in SGE:
        assert sge(bits(a), b) == y
        assert sge(a, bits(b)) == y

    # Invalid rhs
    with pytest.raises(TypeError):
        sge("1b0", "2b00")


MATCH = [
    ("2b00", "2b00", T),
    ("2b00", "2b01", F),
    ("2b00", "2b0X", X),
    ("2b00", "2bX0", X),
    ("2b00", "2b0-", T),
    ("2b00", "2b-0", T),
    ("2b10", "2b10", T),
    ("2b10", "2b11", F),
    ("2b10", "2b1X", X),
    ("2b10", "2bX1", X),
    ("2b10", "2b1-", T),
    ("2b10", "2b-0", T),
]


def test_match():
    for a, b, y in MATCH:
        assert match(bits(a), b) == y
        assert match(a, bits(b)) == y
