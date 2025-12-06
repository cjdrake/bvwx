"""Predicate Operators"""

import operator
from collections.abc import Callable

from ._bits import (
    Array,
    ArrayLike,
    Scalar,
    bits_uand,
    bits_uor,
    bits_xnor,
    bits_xor,
    bool2scalar,
    expect_array,
    expect_array_size,
    scalar0,
    scalar1,
    scalarW,
    scalarX,
)


def _eq(x0: Array, x1: Array) -> Scalar:
    return bits_uand(bits_xnor(x0, x1))


def eq(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _eq(x0, x1)


def _ne(x0: Array, x1: Array) -> Scalar:
    return bits_uor(bits_xor(x0, x1))


def ne(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _ne(x0, x1)


def _cmp(op: Callable[[int, int], bool], x0: Array, x1: Array) -> Scalar:
    # X/W propagation
    if x0.has_x() or x1.has_x():
        return scalarX
    if x0.has_w() or x1.has_w():
        return scalarW
    return bool2scalar[op(x0.to_uint(), x1.to_uint())]


def lt(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _cmp(operator.lt, x0, x1)


def le(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _cmp(operator.le, x0, x1)


def gt(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _cmp(operator.gt, x0, x1)


def ge(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _cmp(operator.ge, x0, x1)


def _scmp(op: Callable[[int, int], bool], x0: Array, x1: Array) -> Scalar:
    # X/W propagation
    if x0.has_x() or x1.has_x():
        return scalarX
    if x0.has_w() or x1.has_w():
        return scalarW
    return bool2scalar[op(x0.to_int(), x1.to_int())]


def slt(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _scmp(operator.lt, x0, x1)


def sle(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _scmp(operator.le, x0, x1)


def sgt(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _scmp(operator.gt, x0, x1)


def sge(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _scmp(operator.ge, x0, x1)


def _match(x0: Array, x1: Array) -> Scalar:
    # Propagate X
    if x0.has_x() or x1.has_x():
        return scalarX

    for i in range(x0.size):
        a0, a1 = x0.get_index(i)
        b0, b1 = x1.get_index(i)
        if a0 ^ b0 and a1 ^ b1:
            return scalar0
    return scalar1


def match(x0: ArrayLike, x1: ArrayLike) -> Scalar:
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
        x0: ``Array`` or string literal.
        x1: ``Array`` or string literal equal size to ``x0``.

    Returns:
        ``Scalar``

    Raises:
        TypeError: ``x0`` or ``x1`` is not a valid ``Array`` object,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    x1 = expect_array_size(x1, x0.size)
    return _match(x0, x1)
