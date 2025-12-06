"""Arithmetic Operators"""

from ._bits import (
    Array,
    ArrayLike,
    ScalarLike,
    UintLike,
    Vector,
    bits_add,
    bits_cat,
    bits_div,
    bits_lsh,
    bits_matmul,
    bits_mod,
    bits_mul,
    bits_neg,
    bits_rsh,
    bits_sub,
    expect_array,
    expect_array_size,
    expect_scalar,
    expect_uint,
    scalar0,
)
from ._util import mask


def add(a: ArrayLike, b: ArrayLike, ci: ScalarLike | None = None) -> Array:
    """Addition with carry-in, but NO carry-out.

    For example:

    >>> add("4d2", "4d2")
    bits("4b0100")

    >>> add("2d2", "2d2")
    bits("2b00")

    Args:
        a: ``Array`` or string literal
        b: ``Array`` or string literal
        ci: ``Scalar`` carry-in, or ``None``.
            ``None`` defaults to carry-in ``0``.

    Returns:
        ``Array`` sum w/ size equal to ``max(a.size, b.size)``.

    Raises:
        TypeError: ``a``, ``b``, or ``ci`` are not valid ``Array`` objects.
        ValueError: Error parsing string literal.
    """
    a = expect_array(a)
    b = expect_array(b)
    ci = scalar0 if ci is None else expect_scalar(ci)
    s, _ = bits_add(a, b, ci)
    return s


def adc(a: ArrayLike, b: ArrayLike, ci: ScalarLike | None = None) -> Vector:
    """Addition with carry-in, and carry-out.

    For example:

    >>> adc("4d2", "4d2")
    bits("5b0_0100")

    >>> adc("2d2", "2d2")
    bits("3b100")

    Args:
        a: ``Array`` or string literal
        b: ``Array`` or string literal
        ci: ``Scalar`` carry-in, or ``None``.
            ``None`` defaults to carry-in ``0``.

    Returns:
        ``Vector`` sum w/ size equal to ``max(a.size, b.size) + 1``.
        The most significant bit is the carry-out.

    Raises:
        TypeError: ``a``, ``b``, or ``ci`` are not valid ``Array`` objects.
        ValueError: Error parsing string literal.
    """
    a = expect_array(a)
    b = expect_array(b)
    ci = scalar0 if ci is None else expect_scalar(ci)
    s, co = bits_add(a, b, ci)
    v = bits_cat(s, co)
    assert isinstance(v, Vector)
    return v


def sub(a: ArrayLike, b: ArrayLike) -> Array:
    """Twos complement subtraction, with NO carry-out.

    Args:
        a: ``Array`` or string literal
        b: ``Array`` or string literal equal size to ``a``.

    Returns:
        ``Array`` sum equal size to ``a`` and ``b``.

    Raises:
        TypeError: ``a``, or ``b`` are not valid ``Array`` objects,
                   or ``a`` not equal size to ``b``.
        ValueError: Error parsing string literal.
    """
    a = expect_array(a)
    b = expect_array_size(b, a.size)
    s, _ = bits_sub(a, b)
    return s


def sbc(a: ArrayLike, b: ArrayLike) -> Vector:
    """Twos complement subtraction, with carry-out.

    Args:
        a: ``Array`` or string literal
        b: ``Array`` or string literal equal size to ``a``.

    Returns:
        ``Array`` sum w/ size one larger than ``a`` and ``b``.
        The most significant bit is the carry-out.

    Raises:
        TypeError: ``a``, or ``b`` are not valid ``Array`` objects,
                   or ``a`` not equal size to ``b``.
        ValueError: Error parsing string literal.
    """
    a = expect_array(a)
    b = expect_array_size(b, a.size)
    s, co = bits_sub(a, b)
    v = bits_cat(s, co)
    assert isinstance(v, Vector)
    return v


def neg(x: ArrayLike) -> Array:
    """Twos complement negation, with NO carry-out.

    Args:
        x: ``Array`` or string literal

    Returns:
        ``Array`` equal size to ``x``.

    Raises:
        TypeError: ``x`` is not a valid ``Array`` object.
        ValueError: Error parsing string literal.
    """
    x = expect_array(x)
    s, _ = bits_neg(x)
    return s


def ngc(x: ArrayLike) -> Vector:
    """Twos complement negation, with carry-out.

    Args:
        x: ``Array`` or string literal

    Returns:
        ``Array`` w/ size one larger than ``x``.
        The most significant bit is the carry-out.

    Raises:
        TypeError: ``x`` is not a valid ``Array`` object.
        ValueError: Error parsing string literal.
    """
    x = expect_array(x)
    s, co = bits_neg(x)
    v = bits_cat(s, co)
    assert isinstance(v, Vector)
    return v


def mul(a: ArrayLike, b: ArrayLike) -> Vector:
    """Unsigned multiply.

    For example:

    >>> mul("4d2", "4d2")
    bits("8b0000_0100")

    >>> add("2d2", "2d2")
    bits("2b00")

    Args:
        a: ``Array`` or string literal
        b: ``Array`` or string literal

    Returns:
        ``Vector`` product w/ size ``a.size + b.size``

    Raises:
        TypeError: ``a`` or ``b`` are not valid ``Array`` objects.
        ValueError: Error parsing string literal.
    """
    a = expect_array(a)
    b = expect_array(b)
    return bits_mul(a, b)


def div(a: ArrayLike, b: ArrayLike) -> Array:
    """Unsigned divide.

    Args:
        a: ``Array`` or string literal
        b: ``Array`` or string literal

    Returns:
        ``Vector`` quotient w/ size ``a.size``

    Raises:
        TypeError: ``a`` or ``b`` are not valid ``Array`` objects.
        ValueError: Error parsing string literal.
        ZeroDivisionError: If ``b`` is zero.
    """
    a = expect_array(a)
    b = expect_array(b)
    return bits_div(a, b)


def mod(a: ArrayLike, b: ArrayLike) -> Array:
    """Unsigned modulo.

    Args:
        a: ``Array`` or string literal
        b: ``Array`` or string literal

    Returns:
        ``Vector`` remainder w/ size ``b.size``

    Raises:
        TypeError: ``a`` or ``b`` are not valid ``Array`` objects.
        ValueError: Error parsing string literal.
        ZeroDivisionError: If ``b`` is zero.
    """
    a = expect_array(a)
    b = expect_array(b)
    return bits_mod(a, b)


def matmul(a: ArrayLike, b: ArrayLike) -> Array:
    """Matrix multiply.

    Args:
        a: ``Array`` or string literal
        b: ``Array`` or string literal

    Returns:
        ``Array`` product

    Raises:
        TypeError: ``a`` or ``b`` are invalid or incompatible ``Array`` objects.
        ValueError: Error parsing string literal.
    """
    a = expect_array(a)
    b = expect_array(b)
    return bits_matmul(a, b)


def lsh(x: ArrayLike, n: UintLike) -> Array:
    """Logical left shift by n bits.

    Fill bits with zeros.

    For example:

    >>> lsh("4b1011", 2)
    bits("4b1100")

    Args:
        x: ``Array`` or string literal.
        n: ``Array``, string literal, or ``int``
           Non-negative bit shift count.

    Returns:
        ``Array`` left-shifted by n bits.

    Raises:
        TypeError: ``x`` is not a valid ``Array`` object,
                   or ``n`` is not a valid bit shift count.
        ValueError: Error parsing string literal,
                    or negative shift amount.
    """
    x = expect_array(x)
    n = expect_uint(n)
    return bits_lsh(x, n)


def rsh(x: ArrayLike, n: UintLike) -> Array:
    """Logical right shift by n bits.

    Fill bits with zeros.

    For example:

    >>> rsh("4b1101", 2)
    bits("4b0011")

    Args:
        x: ``Array`` or string literal.
        n: ``Array``, string literal, or ``int``
           Non-negative bit shift count.

    Returns:
        ``Array`` right-shifted by n bits.

    Raises:
        TypeError: ``x`` is not a valid ``Array`` object,
                   or ``n`` is not a valid bit shift count.
        ValueError: Error parsing string literal,
                    or negative shift amount.
    """
    x = expect_array(x)
    n = expect_uint(n)
    return bits_rsh(x, n)


def _srsh[T: Array](x: T, n: Array) -> T:
    if n.has_x():
        return x.xs()
    if n.has_w():
        return x.ws()

    _n = n.to_uint()
    if _n == 0:
        return x
    if _n > x.size:
        raise ValueError(f"Expected n ≤ {x.size}, got {_n}")

    sign0, sign1 = x.get_index(x.size - 1)
    si0, si1 = mask(_n) * sign0, mask(_n) * sign1

    sh_size, (sh0, sh1) = x.get_slice(_n, x.size)
    d0 = sh0 | si0 << sh_size
    d1 = sh1 | si1 << sh_size
    y = x.cast_data(d0, d1)

    return y


def srsh(x: ArrayLike, n: UintLike) -> Array:
    """Arithmetic (signed) right shift by n bits.

    Fill bits with most significant bit (sign).

    For example:

    >>> srsh("4b1101", 2)
    bits("4b1111")

    Args:
        x: ``Array`` or string literal.
        n: ``Array``, string literal, or ``int``
           Non-negative bit shift count.

    Returns:
        ``Array`` right-shifted by n bits.

    Raises:
        TypeError: ``x`` is not a valid ``Array`` object,
                   or ``n`` is not a valid bit shift count.
        ValueError: Error parsing string literal,
                    or negative shift amount.
    """
    x = expect_array(x)
    n = expect_uint(n)
    return _srsh(x, n)
