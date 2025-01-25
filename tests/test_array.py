"""Test bvwx Array"""

# pylint: disable=pointless-statement
# pylint: disable=comparison-with-callable

import pytest

from bvwx import Array, Vector, bits
from bvwx._lbool import _W, _X, _0, _1

E = Array[0](*_X)

X = Array[1](*_X)
F = Array[1](*_0)
T = Array[1](*_1)
W = Array[1](*_W)


def test_basic():
    # empty len, getitem, iter
    assert len(E) == 0
    with pytest.raises(IndexError):
        E[0]
    assert not list(E)

    # Scalar len, getitem, iter
    assert len(F) == 1
    assert F[0] == F
    assert list(F) == [F]

    # Degenerate dimensions
    assert Array[0] is Vector[0]
    assert Array[1] is Vector[1]
    assert Array[2] is Vector[2]

    # Invalid dimension lens
    with pytest.raises(TypeError):
        _ = Array[2, 0, 3]
    with pytest.raises(TypeError):
        _ = Array[2, -1, 3]
    with pytest.raises(TypeError):
        _ = Array[0, 2, 2]

    b = Array[2, 3, 4](0, 0)

    # Class attributes
    assert b.shape == (2, 3, 4)
    assert b.size == 24

    # Basic methods
    assert b.flatten() == Vector[24](0, 0)
    assert b.reshape((4, 3, 2)) == Array[4, 3, 2](0, 0)
    with pytest.raises(ValueError):
        b.reshape((4, 4, 4))
    # assert list(b.flat) == [Vec[1](0, 0)] * 24


def test_rank2_errors():
    """Test bits function rank2 errors."""
    # Mismatched str literal
    with pytest.raises(TypeError):
        bits(["4b-10X", "3b10X"])
    # bits followed by some invalid type
    with pytest.raises(TypeError):
        bits(["4b-10X", 42])


R3VEC = """\
[[4b-10X, 4b-10X],
 [4b-10X, 4b-10X]]"""


def test_rank3_vec():
    """Test bits function w/ rank3 input."""
    b = bits(
        [
            ["4b-10X", "4b-10X"],
            ["4b-10X", "4b-10X"],
        ]
    )

    assert b.flatten() == bits("16b-10X_-10X_-10X_-10X")

    # Test __str__
    assert str(b) == R3VEC


R4VEC = """\
[[[4b-10X, 4b-10X],
  [4b-10X, 4b-10X]],

 [[4b-10X, 4b-10X],
  [4b-10X, 4b-10X]]]"""


def test_rank4_vec():
    """Test bits function w/ rank4 input."""
    b = bits(
        [
            [["4b-10X", "4b-10X"], ["4b-10X", "4b-10X"]],
            [["4b-10X", "4b-10X"], ["4b-10X", "4b-10X"]],
        ]
    )

    # Test __str__
    assert str(b) == R4VEC


def test_invalid_vec():
    """Test bits function invalid input."""
    with pytest.raises(TypeError):
        bits(42)
