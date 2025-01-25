"""Test bvwx Union"""

# For error testing
# pylint: disable=unused-variable
# pylint: disable=unsubscriptable-object

import pytest

from bvwx import Union, Vector, bits


def test_empty():
    with pytest.raises(ValueError):

        class EmptyUnion(Union):
            pass


class Simple(Union):
    a: Vector[2]
    b: Vector[3]
    c: Vector[4]


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


def test_init():
    u = Simple("2b00")
    assert str(u) == "Simple(\n    a=2b00,\n    b=3bX00,\n    c=4bXX00,\n)"
    u = Simple("3b000")
    assert str(u) == "Simple(\n    a=2b00,\n    b=3b000,\n    c=4bX000,\n)"
    u = Simple("4b0000")
    assert str(u) == "Simple(\n    a=2b00,\n    b=3b000,\n    c=4b0000,\n)"

    with pytest.raises(TypeError):
        _ = Simple(bits("8h0000"))
