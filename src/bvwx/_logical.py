"""Logical Operators"""

from . import _lbool as lb
from ._bits import Array, ScalarLike, expect_scalar, scalar_obj


def _lor(*xs: Array) -> Array:
    y = lb.F
    for x in xs:
        y = lb.or_(y, x._data)
    return scalar_obj(*y)


def lor(*xs: ScalarLike) -> Array:
    """N-ary logical OR operator.

    The identity of OR is ``0``.

    For example:

    >>> lor(False, 0, "1b1")
    bits("1b1")

    Empty input returns identity:

    >>> lor()
    bits("1b0")

    Args:
        xs: Sequence of bool / Scalar / string literal.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x`` is not a valid ``Scalar`` object.
        ValueError: Error parsing string literal.
    """
    return _lor(*[expect_scalar(x) for x in xs])


def _land(*xs: Array) -> Array:
    y = lb.T
    for x in xs:
        y = lb.and_(y, x._data)
    return scalar_obj(*y)


def land(*xs: ScalarLike) -> Array:
    """N-ary logical AND operator.

    The identity of AND is ``1``.

    For example:

    >>> land(True, 1, "1b0")
    bits("1b0")

    Empty input returns identity:

    >>> land()
    bits("1b1")

    Args:
        xs: Sequence of bool / Scalar / string literal.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x`` is not a valid ``Scalar`` object.
        ValueError: Error parsing string literal.
    """
    return _land(*[expect_scalar(x) for x in xs])


def _lxor(*xs: Array) -> Array:
    y = lb.F
    for x in xs:
        y = lb.xor(y, x._data)
    return scalar_obj(*y)


def lxor(*xs: ScalarLike) -> Array:
    """N-ary logical XOR operator.

    The identity of XOR is ``0``.

    For example:

    >>> lxor(False, 0, "1b1")
    bits("1b1")

    Empty input returns identity:

    >>> lxor()
    bits("1b0")

    Args:
        xs: Sequence of bool / Scalar / string literal.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x`` is not a valid ``Scalar`` object.
        ValueError: Error parsing string literal.
    """
    return _lxor(*[expect_scalar(x) for x in xs])
