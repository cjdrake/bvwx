"""Unary Reduction Operators"""

from ._bits import Bits, Scalar, _expect_type, _uand, _uor, _uxor


def uor(x: Bits | str) -> Scalar:
    """Unary OR reduction operator.

    The identity of OR is ``0``.
    Compute an OR-sum over all the bits of ``x``.

    For example:

    >>> uor("4b1000")
    bits("1b1")

    Empty input returns identity:

    >>> from bvwx import bits
    >>> uor(bits())
    bits("1b0")

    Args:
        x: ``Bits`` or string literal.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: Error parsing string literal.
    """
    x = _expect_type(x, Bits)
    return _uor(x)


def uand(x: Bits | str) -> Scalar:
    """Unary AND reduction operator.

    The identity of AND is ``1``.
    Compute an AND-sum over all the bits of ``x``.

    For example:

    >>> uand("4b0111")
    bits("1b0")

    Empty input returns identity:

    >>> from bvwx import bits
    >>> uand(bits())
    bits("1b1")

    Args:
        x: ``Bits`` or string literal.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: Error parsing string literal.
    """
    x = _expect_type(x, Bits)
    return _uand(x)


def uxor(x: Bits | str) -> Scalar:
    """Unary XOR reduction operator.

    The identity of XOR is ``0``.
    Compute an XOR-sum (odd parity) over all the bits of ``x``.

    For example:

    >>> uxor("4b1010")
    bits("1b0")

    Empty input returns identity:

    >>> from bvwx import bits
    >>> uxor(bits())
    bits("1b0")

    Args:
        x: ``Bits`` or string literal.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: Error parsing string literal.
    """
    x = _expect_type(x, Bits)
    return _uxor(x)
