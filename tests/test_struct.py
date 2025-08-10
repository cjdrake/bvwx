"""Test bvwx Struct."""

# pyright: reportCallIssue=false

import pytest

from bvwx import Struct, Vec


def test_empty():
    with pytest.raises(ValueError):

        class EmptyStruct(Struct):  # pyright: ignore[reportUnusedClass]
            pass


class Simple(Struct):
    a: Vec[2]
    b: Vec[3]
    c: Vec[4]


class Compound(Struct):
    p: Simple
    q: Simple


S1 = """\
Simple(
    a=2b10,
    b=3b011,
    c=4b0100,
)"""

R1 = """\
Simple(
    a=bits("2b10"),
    b=bits("3b011"),
    c=bits("4b0100"),
)"""


def test_simple():
    s = Simple(a="2b10", b="3b011", c="4b0100")

    assert str(s.a) == "2b10"
    assert str(s.b) == "3b011"
    assert str(s.c) == "4b0100"

    assert str(s) == S1
    assert repr(s) == R1

    assert s[0] == s.a[0]
    assert s[1] == s.a[1]
    assert s[2] == s.b[0]
    assert s[3] == s.b[1]
    assert s[4] == s.b[2]
    assert s[5] == s.c[0]
    assert s[6] == s.c[1]
    assert s[7] == s.c[2]
    assert s[8] == s.c[3]


S2 = """\
Compound(
    p=Simple(
        a=2b01,
        b=3b010,
        c=4b0011,
    ),
    q=Simple(
        a=2b10,
        b=3b100,
        c=4b1000,
    ),
)"""

R2 = """\
Compound(
    p=Simple(
        a=bits("2b01"),
        b=bits("3b010"),
        c=bits("4b0011"),
    ),
    q=Simple(
        a=bits("2b10"),
        b=bits("3b100"),
        c=bits("4b1000"),
    ),
)"""


def test_compound():
    c = Compound(
        p=Simple(a="2b01", b="3b010", c="4b0011"),
        q=Simple(a="2b10", b="3b100", c="4b1000"),
    )

    assert str(c) == S2
    assert repr(c) == R2


def test_init():
    s = Simple()
    assert str(s) == "Simple(\n    a=2bXX,\n    b=3bXXX,\n    c=4bXXXX,\n)"
    s = Simple(a="2b11")
    assert str(s) == "Simple(\n    a=2b11,\n    b=3bXXX,\n    c=4bXXXX,\n)"
    s = Simple(b="3b111")
    assert str(s) == "Simple(\n    a=2bXX,\n    b=3b111,\n    c=4bXXXX,\n)"
    s = Simple(c="4b1111")
    assert str(s) == "Simple(\n    a=2bXX,\n    b=3bXXX,\n    c=4b1111,\n)"

    assert str(Simple.xs()) == "Simple(\n    a=2bXX,\n    b=3bXXX,\n    c=4bXXXX,\n)"
    assert str(Simple.dcs()) == "Simple(\n    a=2b--,\n    b=3b---,\n    c=4b----,\n)"
