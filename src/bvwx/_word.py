"""Word Operators"""

from ._bits import (
    Bits,
    BitsLike,
    UintLike,
    Vector,
    _cat,
    bool2scalar,
    expect_bits,
    expect_uint,
    lit2bv,
    vec_size,
)
from ._util import mask


def _xt[T: Bits](x: T, n: Bits) -> T | Vector:
    if n.has_x:
        return x.xes()
    if n.has_w:
        return x.dcs()

    _n = n.to_uint()
    if _n == 0:
        return x

    ext0 = mask(_n)
    d0 = x.data[0] | ext0 << x.size
    d1 = x.data[1]
    return vec_size(x.size + _n)(d0, d1)


def xt(x: BitsLike, n: UintLike) -> Bits:
    """Unsigned extend by n bits.

    Fill high order bits with zero.

    For example:

    >>> xt("2b11", 2)
    bits("4b0011")

    Args:
        x: ``Bits`` or string literal.
        n: Non-negative number of bits.

    Returns:
        ``Bits`` zero-extended by n bits.

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: If n is negative.
    """
    x = expect_bits(x)
    n = expect_uint(n)
    return _xt(x, n)


def _sxt[T: Bits](x: T, n: Bits) -> T | Vector:
    # Empty does not have a sign
    if x.size == 0:
        raise TypeError("Cannot sign extend empty")

    if n.has_x:
        return x.xes()
    if n.has_w:
        return x.dcs()

    _n = n.to_uint()
    if _n == 0:
        return x

    sign0, sign1 = x.get_index(x.size - 1)
    ext0 = mask(_n) * sign0
    ext1 = mask(_n) * sign1
    d0 = x.data[0] | ext0 << x.size
    d1 = x.data[1] | ext1 << x.size
    return vec_size(x.size + _n)(d0, d1)


def sxt(x: BitsLike, n: UintLike) -> Bits:
    """Sign extend by n bits.

    Fill high order bits with sign.

    For example:

    >>> sxt("2b11", 2)
    bits("4b1111")

    Args:
        x: ``Bits`` or string literal.
        n: Non-negative number of bits.

    Returns:
        ``Bits`` sign-extended by n bits.

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object, or empty.
        ValueError: If n is negative.
    """
    x = expect_bits(x)
    n = expect_uint(n)
    return _sxt(x, n)


def _lrot[T: Bits](x: T, n: Bits) -> T:
    if n.has_x:
        return x.xes()
    if n.has_w:
        return x.dcs()

    _n = n.to_uint()
    if _n == 0:
        return x
    if _n >= x.size:
        raise ValueError(f"Expected n < {x.size}, got {_n}")

    _, (co0, co1) = x.get_slice(x.size - _n, x.size)
    _, (sh0, sh1) = x.get_slice(0, x.size - _n)
    d0 = co0 | sh0 << _n
    d1 = co1 | sh1 << _n
    return x.cast_data(d0, d1)


def lrot(x: BitsLike, n: UintLike) -> Bits:
    """Rotate left by n bits.

    For example:

    >>> lrot("4b1011", 2)
    bits("4b1110")

    Args:
        x: ``Bits`` or string literal.
        n: ``Bits``, string literal, or ``int``
           Non-negative bit rotate count.

    Returns:
        ``Bits`` left-rotated by n bits.

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object,
                   or ``n`` is not a valid bit rotate count.
        ValueError: Error parsing string literal,
                    or negative rotate amount.
    """
    x = expect_bits(x)
    n = expect_uint(n)
    return _lrot(x, n)


def _rrot[T: Bits](x: T, n: Bits) -> T:
    if n.has_x:
        return x.xes()
    if n.has_w:
        return x.dcs()

    _n = n.to_uint()
    if _n == 0:
        return x
    if _n >= x.size:
        raise ValueError(f"Expected n < {x.size}, got {_n}")

    _, (co0, co1) = x.get_slice(0, _n)
    sh_size, (sh0, sh1) = x.get_slice(_n, x.size)
    d0 = sh0 | co0 << sh_size
    d1 = sh1 | co1 << sh_size
    return x.cast_data(d0, d1)


def rrot(x: BitsLike, n: UintLike) -> Bits:
    """Rotate right by n bits.

    For example:

    >>> rrot("4b1101", 2)
    bits("4b0111")

    Args:
        x: ``Bits`` or string literal.
        n: ``Bits``, string literal, or ``int``
           Non-negative bit rotate count.

    Returns:
        ``Bits`` right-rotated by n bits.

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object,
                   or ``n`` is not a valid bit rotate count.
        ValueError: Error parsing string literal,
                    or negative rotate amount.
    """
    x = expect_bits(x)
    n = expect_uint(n)
    return _rrot(x, n)


def cat(*objs: BitsLike) -> Bits:
    """Concatenate a sequence of Vectors.

    Args:
        objs: a sequence of vec/bool/lit objects.

    Returns:
        A Vec instance.

    Raises:
        TypeError: If input obj is invalid.
    """
    # Convert inputs
    xs: list[Bits] = []
    for obj in objs:
        if isinstance(obj, int) and obj in (0, 1):
            xs.append(bool2scalar[obj])
        elif isinstance(obj, str):
            x = lit2bv(obj)
            xs.append(x)
        elif isinstance(obj, Bits):
            xs.append(obj)
        else:
            raise TypeError(f"Invalid input: {obj}")

    return _cat(*xs)


def rep(obj: BitsLike, n: int) -> Bits:
    """Repeat a Vector n times."""
    objs = [obj] * n
    return cat(*objs)


def _pack[T: Bits](x: T, n: int) -> T:
    if n < 1:
        raise ValueError(f"Expected n ≥ 1, got {n}")
    if x.size % n != 0:
        raise ValueError("Expected x.size to be a multiple of n")

    if x.size == 0:
        return x

    m = mask(n)
    xd0, xd1 = x.data
    d0, d1 = xd0 & m, xd1 & m
    for _ in range(n, x.size, n):
        xd0 >>= n
        xd1 >>= n
        d0 = (d0 << n) | (xd0 & m)
        d1 = (d1 << n) | (xd1 & m)

    return x.cast_data(d0, d1)


def pack(x: BitsLike, n: int = 1) -> Bits:
    """Pack n-bit blocks in right to left order."""
    x = expect_bits(x)
    return _pack(x, n)
