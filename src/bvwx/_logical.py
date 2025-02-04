"""Logical Operators"""

from ._bits import Scalar, _expect_type, _land_, _lor_, _lxor_


def lor(*xs: Scalar | str) -> Scalar:
    """N-ary logical OR operator."""
    return _lor_(*[_expect_type(x, Scalar) for x in xs])


def land(*xs: Scalar | str) -> Scalar:
    """N-ary logical AND operator."""
    return _land_(*[_expect_type(x, Scalar) for x in xs])


def lxor(*xs: Scalar | str) -> Scalar:
    """N-ary logical XOR operator."""
    return _lxor_(*[_expect_type(x, Scalar) for x in xs])
