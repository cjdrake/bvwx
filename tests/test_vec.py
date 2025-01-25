"""Test bvwx Vector"""

import pytest

from bvwx import Vector, bits
from bvwx._lbool import _W, _X, _0, _1

E = Vector[0](*_X)
X = Vector[1](*_X)
F = Vector[1](*_0)
T = Vector[1](*_1)
W = Vector[1](*_W)


def test_vec_class_getitem():
    # Negative values are illegal
    with pytest.raises(TypeError):
        _ = Vector[-1]

    vec_0 = Vector[0]
    assert vec_0.size == 0

    vec_4 = Vector[4]
    assert vec_4.size == 4

    # Always return the same class instance
    assert Vector[0] is vec_0
    assert Vector[4] is vec_4


def test_vec():
    # None/Empty
    assert bits() == E
    assert bits(None) == E
    assert bits([]) == E

    # Single bool input
    assert bits(False) == F
    assert bits(0) == F
    assert bits(True) == T
    assert bits(1) == T

    # Sequence of bools
    assert bits([False, True, 0, 1]) == Vector[4](0b0101, 0b1010)

    # String
    assert bits("4b-10X") == Vector[4](0b1010, 0b1100)

    # Invalid input type
    with pytest.raises(TypeError):
        bits(1.0e42)
    with pytest.raises(TypeError):
        bits([0, 0, 0, 42])


def test_vec_getitem():
    v = bits("4b-10X")

    assert v[3] == "1b-"
    assert v[2] == "1b1"
    assert v[1] == "1b0"
    assert v[0] == "1bX"

    assert v[-1] == "1b-"
    assert v[-2] == "1b1"
    assert v[-3] == "1b0"
    assert v[-4] == "1bX"

    assert v[0:1] == "1bX"
    assert v[0:2] == "2b0X"
    assert v[0:3] == "3b10X"
    assert v[0:4] == "4b-10X"

    assert v[:-3] == "1bX"
    assert v[:-2] == "2b0X"
    assert v[:-1] == "3b10X"

    assert v[1:2] == "1b0"
    assert v[1:3] == "2b10"
    assert v[1:4] == "3b-10"

    assert v[-3:2] == "1b0"
    assert v[-3:3] == "2b10"
    assert v[-3:4] == "3b-10"

    assert v[2:3] == "1b1"
    assert v[2:4] == "2b-1"

    assert v[3:4] == "1b-"

    # Invalid index
    with pytest.raises(IndexError):
        _ = v[4]
    # Slice step not supported
    with pytest.raises(ValueError):
        _ = v[0:4:1]
    # Invalid index type
    with pytest.raises(TypeError):
        _ = v[1.0e42]


def test_vec_iter():
    v = bits("4b-10X")
    assert list(v) == ["1bX", "1b0", "1b1", "1b-"]


def test_vec_repr():
    assert repr(bits()) == "bits([])"
    assert repr(bits("1b0")) == 'bits("1b0")'
    assert repr(bits("4b-10X")) == 'bits("4b-10X")'


def test_vec_bool():
    assert bool(bits()) is False
    assert bool(bits("1b0")) is False
    assert bool(bits("1b1")) is True
    assert bool(bits("4b0000")) is False
    assert bool(bits("4b1010")) is True
    assert bool(bits("4b0101")) is True
    with pytest.raises(ValueError):
        bool(bits("4b110X"))
    with pytest.raises(ValueError):
        bool(bits("4b-100"))


def test_vec_int():
    assert int(bits()) == 0
    assert int(bits("1b0")) == 0
    assert int(bits("1b1")) == -1
    assert int(bits("4b0000")) == 0
    assert int(bits("4b1010")) == -6
    assert int(bits("4b0101")) == 5
    with pytest.raises(ValueError):
        int(bits("4b110X"))
    with pytest.raises(ValueError):
        int(bits("4b-100"))


def test_reshape():
    v = bits("4b1010")
    assert v.reshape(v.shape) is v
    assert v.flatten() is v
    with pytest.raises(ValueError):
        v.reshape((5,))
    assert str(v.reshape((2, 2))) == "[2b10, 2b10]"
