"""Logical Operators"""

from ._bits import Scalar, ScalarLike, _land_, _lor_, _lxor_, expect_scalar


def lor(*xs: ScalarLike) -> Scalar:
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
    return _lor_(*[expect_scalar(x) for x in xs])


def land(*xs: ScalarLike) -> Scalar:
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
    return _land_(*[expect_scalar(x) for x in xs])


def lxor(*xs: ScalarLike) -> Scalar:
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
    return _lxor_(*[expect_scalar(x) for x in xs])
