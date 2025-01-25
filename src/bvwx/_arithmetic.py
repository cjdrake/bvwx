"""Arithmetic Operators"""

from ._bits import (
    Bits,
    Scalar,
    Vector,
    _add,
    _cat,
    _div,
    _expect_shift,
    _expect_size,
    _expect_type,
    _lsh,
    _mod,
    _mul,
    _neg,
    _rsh,
    _Scalar0,
    _srsh,
    _sub,
)


def add(a: Bits | str, b: Bits | str, ci: Scalar | str | None = None) -> Bits:
    """Addition with carry-in, but NO carry-out.

    For example:

    >>> add("4d2", "4d2")
    bits("4b0100")

    >>> add("2d2", "2d2")
    bits("2b00")

    Args:
        a: ``Bits`` or string literal
        b: ``Bits`` or string literal
        ci: ``Scalar`` carry-in, or ``None``.
            ``None`` defaults to carry-in ``0``.

    Returns:
        ``Bits`` sum w/ size equal to ``max(a.size, b.size)``.

    Raises:
        TypeError: ``a``, ``b``, or ``ci`` are not valid ``Bits`` objects.
        ValueError: Error parsing string literal.
    """
    a = _expect_type(a, Bits)
    b = _expect_type(b, Bits)
    ci = _Scalar0 if ci is None else _expect_type(ci, Scalar)
    s, _ = _add(a, b, ci)
    return s


def adc(a: Bits | str, b: Bits | str, ci: Scalar | str | None = None) -> Vector:
    """Addition with carry-in, and carry-out.

    For example:

    >>> adc("4d2", "4d2")
    bits("5b0_0100")

    >>> adc("2d2", "2d2")
    bits("3b100")

    Args:
        a: ``Bits`` or string literal
        b: ``Bits`` or string literal
        ci: ``Scalar`` carry-in, or ``None``.
            ``None`` defaults to carry-in ``0``.

    Returns:
        ``Vector`` sum w/ size equal to ``max(a.size, b.size) + 1``.
        The most significant bit is the carry-out.

    Raises:
        TypeError: ``a``, ``b``, or ``ci`` are not valid ``Bits`` objects.
        ValueError: Error parsing string literal.
    """
    a = _expect_type(a, Bits)
    b = _expect_type(b, Bits)
    ci = _Scalar0 if ci is None else _expect_type(ci, Scalar)
    s, co = _add(a, b, ci)
    return _cat(s, co)


def sub(a: Bits | str, b: Bits | str) -> Bits:
    """Twos complement subtraction, with NO carry-out.

    Args:
        a: ``Bits`` or string literal
        b: ``Bits`` or string literal equal size to ``a``.

    Returns:
        ``Bits`` sum equal size to ``a`` and ``b``.

    Raises:
        TypeError: ``a``, or ``b`` are not valid ``Bits`` objects,
                   or ``a`` not equal size to ``b``.
        ValueError: Error parsing string literal.
    """
    a = _expect_type(a, Bits)
    b = _expect_size(b, a.size)
    s, _ = _sub(a, b)
    return s


def sbc(a: Bits | str, b: Bits | str) -> Vector:
    """Twos complement subtraction, with carry-out.

    Args:
        a: ``Bits`` or string literal
        b: ``Bits`` or string literal equal size to ``a``.

    Returns:
        ``Bits`` sum w/ size one larger than ``a`` and ``b``.
        The most significant bit is the carry-out.

    Raises:
        TypeError: ``a``, or ``b`` are not valid ``Bits`` objects,
                   or ``a`` not equal size to ``b``.
        ValueError: Error parsing string literal.
    """
    a = _expect_type(a, Bits)
    b = _expect_size(b, a.size)
    s, co = _sub(a, b)
    return _cat(s, co)


def neg(x: Bits | str) -> Bits:
    """Twos complement negation, with NO carry-out.

    Args:
        x: ``Bits`` or string literal

    Returns:
        ``Bits`` equal size to ``x``.

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: Error parsing string literal.
    """
    x = _expect_type(x, Bits)
    s, _ = _neg(x)
    return s


def ngc(x: Bits | str) -> Vector:
    """Twos complement negation, with carry-out.

    Args:
        x: ``Bits`` or string literal

    Returns:
        ``Bits`` w/ size one larger than ``x``.
        The most significant bit is the carry-out.

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: Error parsing string literal.
    """
    x = _expect_type(x, Bits)
    s, co = _neg(x)
    return _cat(s, co)


def mul(a: Bits | str, b: Bits | str) -> Vector:
    """Unsigned multiply.

    For example:

    >>> mul("4d2", "4d2")
    bits("8b0000_0100")

    >>> add("2d2", "2d2")
    bits("2b00")

    Args:
        a: ``Bits`` or string literal
        b: ``Bits`` or string literal

    Returns:
        ``Vector`` product w/ size ``a.size + b.size``

    Raises:
        TypeError: ``a`` or ``b`` are not valid ``Bits`` objects.
        ValueError: Error parsing string literal.
    """
    a = _expect_type(a, Bits)
    b = _expect_type(b, Bits)
    return _mul(a, b)


def div(a: Bits | str, b: Bits | str) -> Bits:
    """Unsigned divide.

    Args:
        a: ``Bits`` or string literal
        b: ``Bits`` or string literal

    Returns:
        ``Vector`` quotient w/ size ``a.size``

    Raises:
        TypeError: ``a`` or ``b`` are not valid ``Bits`` objects.
        ValueError: Error parsing string literal.
    """
    a = _expect_type(a, Bits)
    b = _expect_type(b, Bits)
    if not a.size >= b.size > 0:
        raise ValueError("Expected a.size ≥ b.size > 0")
    return _div(a, b)


def mod(a: Bits | str, b: Bits | str) -> Bits:
    """Unsigned modulo.

    Args:
        a: ``Bits`` or string literal
        b: ``Bits`` or string literal

    Returns:
        ``Vector`` remainder w/ size ``b.size``

    Raises:
        TypeError: ``a`` or ``b`` are not valid ``Bits`` objects.
        ValueError: Error parsing string literal.
    """
    a = _expect_type(a, Bits)
    b = _expect_type(b, Bits)
    if not a.size >= b.size > 0:
        raise ValueError("Expected a.size ≥ b.size > 0")
    return _mod(a, b)


def lsh(x: Bits | str, n: Bits | str | int) -> Bits:
    """Logical left shift by n bits.

    Fill bits with zeros.

    For example:

    >>> lsh("4b1011", 2)
    bits("4b1100")

    Args:
        x: ``Bits`` or string literal.
        n: ``Bits``, string literal, or ``int``
           Non-negative bit shift count.

    Returns:
        ``Bits`` left-shifted by n bits.

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object,
                   or ``n`` is not a valid bit shift count.
        ValueError: Error parsing string literal,
                    or negative shift amount.
    """
    x = _expect_type(x, Bits)
    n = _expect_shift(n, x.size)
    return _lsh(x, n)


def rsh(x: Bits | str, n: Bits | str | int) -> Bits:
    """Logical right shift by n bits.

    Fill bits with zeros.

    For example:

    >>> rsh("4b1101", 2)
    bits("4b0011")

    Args:
        x: ``Bits`` or string literal.
        n: ``Bits``, string literal, or ``int``
           Non-negative bit shift count.

    Returns:
        ``Bits`` right-shifted by n bits.

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object,
                   or ``n`` is not a valid bit shift count.
        ValueError: Error parsing string literal,
                    or negative shift amount.
    """
    x = _expect_type(x, Bits)
    n = _expect_shift(n, x.size)
    return _rsh(x, n)


def srsh(x: Bits | str, n: Bits | str | int) -> Bits:
    """Arithmetic (signed) right shift by n bits.

    Fill bits with most significant bit (sign).

    For example:

    >>> srsh("4b1101", 2)
    bits("4b1111")

    Args:
        x: ``Bits`` or string literal.
        n: ``Bits``, string literal, or ``int``
           Non-negative bit shift count.

    Returns:
        ``Bits`` right-shifted by n bits.

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object,
                   or ``n`` is not a valid bit shift count.
        ValueError: Error parsing string literal,
                    or negative shift amount.
    """
    x = _expect_type(x, Bits)
    n = _expect_shift(n, x.size)
    return _srsh(x, n)
