"""Logical Operators"""

from ._bits import Scalar, _bool2scalar, _land_, _lit2bv, _lor_, _lxor_


def _expect_scalar(arg) -> Scalar:
    if arg in (0, 1):
        x = _bool2scalar[arg]
    elif isinstance(arg, str):
        x = _lit2bv(arg)
    else:
        x = arg
    if not isinstance(x, Scalar):
        raise TypeError("Expected arg to be Scalar, str literal, or bool")
    return x


def lor(*xs: Scalar | str) -> Scalar:
    """N-ary logical OR operator."""
    return _lor_(*[_expect_scalar(x) for x in xs])


def land(*xs: Scalar | str) -> Scalar:
    """N-ary logical AND operator."""
    return _land_(*[_expect_scalar(x) for x in xs])


def lxor(*xs: Scalar | str) -> Scalar:
    """N-ary logical XOR operator."""
    return _lxor_(*[_expect_scalar(x) for x in xs])
