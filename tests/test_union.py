"""Test bvwx Union"""

# For error testing
# pylint: disable=unused-variable
# pylint: disable=unsubscriptable-object

import pytest

from bvwx import Union, Vec, bits


def test_empty():
    with pytest.raises(ValueError):

        class EmptyUnion(Union):
            pass


class Simple(Union):
    a: Vec[2]
    b: Vec[3]
    c: Vec[4]


class Compound(Union):
    p: Simple
    q: Simple


S1 = """\
Simple(
    a=2b00,
    b=3b000,
    c=4bX000,
)"""

R1 = """\
Simple(
    a=bits("2b00"),
    b=bits("3b000"),
    c=bits("4bX000"),
)"""


def test_simple():
    u = Simple("3b000")

    assert str(u.a) == "2b00"
    assert str(u.b) == "3b000"
    assert str(u.c) == "4bX000"

    assert str(u) == S1
    assert repr(u) == R1

    assert u.size == 4

    assert u[0] == "1b0"
    assert u[1] == "1b0"
    assert u[2] == "1b0"
    assert u[3] == "1bX"


S2 = """\
Compound(
    p=Simple(
        a=2b00,
        b=3b000,
        c=4b0000,
    ),
    q=Simple(
        a=2b00,
        b=3b000,
        c=4b0000,
    ),
)"""

R2 = """\
Compound(
    p=Simple(
        a=bits("2b00"),
        b=bits("3b000"),
        c=bits("4b0000"),
    ),
    q=Simple(
        a=bits("2b00"),
        b=bits("3b000"),
        c=bits("4b0000"),
    ),
)"""


def test_compound():
    c = Compound(Simple("4b0000"))

    assert str(c) == S2
    assert repr(c) == R2


def test_init():
    u = Simple("2b00")
    assert str(u) == "Simple(\n    a=2b00,\n    b=3bX00,\n    c=4bXX00,\n)"
    u = Simple("3b000")
    assert str(u) == "Simple(\n    a=2b00,\n    b=3b000,\n    c=4bX000,\n)"
    u = Simple("4b0000")
    assert str(u) == "Simple(\n    a=2b00,\n    b=3b000,\n    c=4b0000,\n)"

    with pytest.raises(TypeError):
        _ = Simple(bits("8h0000"))
