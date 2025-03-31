"""Word Operators"""

from ._bits import (
    Bits,
    BitsLike,
    UintLike,
    Vector,
    _cat,
    _lrot,
    _pack,
    _rrot,
    _sxt,
    _xt,
    bool2scalar,
    expect_bits,
    expect_uint,
    lit2bv,
)


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


def cat(*objs: BitsLike) -> Vector:
    """Concatenate a sequence of Vectors.

    Args:
        objs: a sequence of vec/bool/lit objects.

    Returns:
        A Vec instance.

    Raises:
        TypeError: If input obj is invalid.
    """
    # Convert inputs
    xs = []
    for obj in objs:
        if obj in (0, 1):
            xs.append(bool2scalar[obj])
        elif isinstance(obj, str):
            x = lit2bv(obj)
            xs.append(x)
        elif isinstance(obj, Bits):
            xs.append(obj)
        else:
            raise TypeError(f"Invalid input: {obj}")

    return _cat(*xs)


def rep(obj: BitsLike, n: int) -> Vector:
    """Repeat a Vector n times."""
    objs = [obj] * n
    return cat(*objs)


def pack(x: BitsLike, n: int = 1) -> Bits:
    """Pack n-bit blocks in right to left order."""
    if n < 1:
        raise ValueError(f"Expected n ≥ 1, got {n}")

    x = expect_bits(x)
    if x.size % n != 0:
        raise ValueError("Expected x.size to be a multiple of n")

    return _pack(x, n)
