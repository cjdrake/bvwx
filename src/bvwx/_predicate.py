"""Predicate Operators"""

import operator

from ._bits import BitsLike, Scalar, _cmp, _eq, _expect_bits, _expect_bits_size, _match, _ne, _scmp


def eq(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Binary logical Equal (==) reduction operator.

    Equivalent to ``uand(xnor(x0, x1))``.

    For example:

    >>> eq("2b01", "2b00")
    bits("1b0")
    >>> eq("2b01", "2b01")
    bits("1b1")
    >>> eq("2b01", "2b10")
    bits("1b0")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _eq(x0, x1)


def ne(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Binary logical NotEqual (!=) reduction operator.

    Equivalent to ``uor(xor(x0, x1))``.

    For example:

    >>> ne("2b01", "2b00")
    bits("1b1")
    >>> ne("2b01", "2b01")
    bits("1b0")
    >>> ne("2b01", "2b10")
    bits("1b1")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _ne(x0, x1)


def lt(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Binary logical Unsigned LessThan (<) reduction operator.

    Returns ``Scalar`` result of ``x0.to_uint() < x1.to_uint()``.
    For performance reasons, use simple ``X``/``-`` propagation:
    ``X`` dominates {``-``, known}, and ``-`` dominates known.

    For example:

    >>> lt("2b01", "2b00")
    bits("1b0")
    >>> lt("2b01", "2b01")
    bits("1b0")
    >>> lt("2b01", "2b10")
    bits("1b1")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _cmp(operator.lt, x0, x1)


def le(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Binary logical Unsigned LessThanOrEqual (≤) reduction operator.

    Returns ``Scalar`` result of ``x0.to_uint() <= x1.to_uint()``.
    For performance reasons, use simple ``X``/``-`` propagation:
    ``X`` dominates {``-``, known}, and ``-`` dominates known.

    For example:

    >>> le("2b01", "2b00")
    bits("1b0")
    >>> le("2b01", "2b01")
    bits("1b1")
    >>> le("2b01", "2b10")
    bits("1b1")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _cmp(operator.le, x0, x1)


def gt(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Binary logical Unsigned GreaterThan (>) reduction operator.

    Returns ``Scalar`` result of ``x0.to_uint() > x1.to_uint()``.
    For performance reasons, use simple ``X``/``-`` propagation:
    ``X`` dominates {``-``, known}, and ``-`` dominates known.

    For example:

    >>> gt("2b01", "2b00")
    bits("1b1")
    >>> gt("2b01", "2b01")
    bits("1b0")
    >>> gt("2b01", "2b10")
    bits("1b0")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _cmp(operator.gt, x0, x1)


def ge(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Binary logical Unsigned GreaterThanOrEqual (≥) reduction operator.

    Returns ``Scalar`` result of ``x0.to_uint() >= x1.to_uint()``.
    For performance reasons, use simple ``X``/``-`` propagation:
    ``X`` dominates {``-``, known}, and ``-`` dominates known.

    For example:

    >>> ge("2b01", "2b00")
    bits("1b1")
    >>> ge("2b01", "2b01")
    bits("1b1")
    >>> ge("2b01", "2b10")
    bits("1b0")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _cmp(operator.ge, x0, x1)


def slt(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Binary logical Signed LessThan (<) reduction operator.

    Returns ``Scalar`` result of ``x0.to_int() < x1.to_int()``.
    For performance reasons, use simple ``X``/``-`` propagation:
    ``X`` dominates {``-``, known}, and ``-`` dominates known.

    For example:

    >>> slt("2b00", "2b11")
    bits("1b0")
    >>> slt("2b00", "2b00")
    bits("1b0")
    >>> slt("2b00", "2b01")
    bits("1b1")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _scmp(operator.lt, x0, x1)


def sle(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Binary logical Signed LessThanOrEqual (≤) reduction operator.

    Returns ``Scalar`` result of ``x0.to_int() <= x1.to_int()``.
    For performance reasons, use simple ``X``/``-`` propagation:
    ``X`` dominates {``-``, known}, and ``-`` dominates known.

    For example:

    >>> sle("2b00", "2b11")
    bits("1b0")
    >>> sle("2b00", "2b00")
    bits("1b1")
    >>> sle("2b00", "2b01")
    bits("1b1")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _scmp(operator.le, x0, x1)


def sgt(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Binary logical Signed GreaterThan (>) reduction operator.

    Returns ``Scalar`` result of ``x0.to_int() > x1.to_int()``.
    For performance reasons, use simple ``X``/``-`` propagation:
    ``X`` dominates {``-``, known}, and ``-`` dominates known.

    For example:

    >>> sgt("2b00", "2b11")
    bits("1b1")
    >>> sgt("2b00", "2b00")
    bits("1b0")
    >>> sgt("2b00", "2b01")
    bits("1b0")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _scmp(operator.gt, x0, x1)


def sge(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Binary logical Signed GreaterThanOrEqual (≥) reduction operator.

    Returns ``Scalar`` result of ``x0.to_int() >= x1.to_int()``.
    For performance reasons, use simple ``X``/``-`` propagation:
    ``X`` dominates {``-``, known}, and ``-`` dominates known.

    For example:

    >>> sge("2b00", "2b11")
    bits("1b1")
    >>> sge("2b00", "2b00")
    bits("1b1")
    >>> sge("2b00", "2b01")
    bits("1b0")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _scmp(operator.ge, x0, x1)


def match(x0: BitsLike, x1: BitsLike) -> Scalar:
    """Pattern match operator.

    Similar to ``eq`` operator, but with support for ``-`` wildcards.

    For example:

    >>> match("2b01", "2b0-")
    bits("1b1")
    >>> match("2b--", "2b10")
    bits("1b1")
    >>> match("2b01", "2b10")
    bits("1b0")

    Args:
        x0: ``Bits`` or string literal.
        x1: ``Bits`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Bits`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = _expect_bits(x0)
    x1 = _expect_bits_size(x1, x0.size)
    return _match(x0, x1)
