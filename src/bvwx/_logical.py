"""Logical Operators"""

from ._bits import Scalar, _bool2scalar, _land_, _lit2bv, _lor_, _lxor_


def _expect_scalar(arg: Scalar | str | bool) -> Scalar:
    if arg in (0, 1):
        x = _bool2scalar[arg]
    elif isinstance(arg, str):
        x = _lit2bv(arg)
    else:
        x = arg
    if not isinstance(x, Scalar):
        raise TypeError("Expected arg to be Scalar, str literal, or bool")
    return x


def lor(*xs: Scalar | str | bool) -> Scalar:
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
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: Error parsing string literal.
    """
    return _lor_(*[_expect_scalar(x) for x in xs])


def land(*xs: Scalar | str | bool) -> Scalar:
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
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: Error parsing string literal.
    """
    return _land_(*[_expect_scalar(x) for x in xs])


def lxor(*xs: Scalar | str | bool) -> Scalar:
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
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: Error parsing string literal.
    """
    return _lxor_(*[_expect_scalar(x) for x in xs])
