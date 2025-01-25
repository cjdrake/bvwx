"""Word Operators"""

from ._bits import (
    Bits,
    Vector,
    _bool2scalar,
    _cat,
    _expect_shift,
    _expect_type,
    _lit2bv,
    _lrot,
    _pack,
    _rrot,
    _sxt,
    _xt,
)


def xt(x: Bits | str, n: int) -> Bits:
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
    x = _expect_type(x, Bits)

    if n < 0:
        raise ValueError(f"Expected n ≥ 0, got {n}")
    if n == 0:
        return x

    return _xt(x, n)


def sxt(x: Bits | str, n: int) -> Bits:
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
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: If n is negative.
    """
    x = _expect_type(x, Bits)

    if n < 0:
        raise ValueError(f"Expected n ≥ 0, got {n}")
    if n == 0:
        return x

    return _sxt(x, n)


def lrot(x: Bits | str, n: Bits | str | int) -> Bits:
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
    x = _expect_type(x, Bits)
    n = _expect_shift(n, x.size)
    return _lrot(x, n)


def rrot(x: Bits | str, n: Bits | str | int) -> Bits:
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
    x = _expect_type(x, Bits)
    n = _expect_shift(n, x.size)
    return _rrot(x, n)


def cat(*objs: Bits | int | str) -> Vector:
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
        if isinstance(obj, Bits):
            xs.append(obj)
        elif obj in (0, 1):
            xs.append(_bool2scalar[obj])
        elif isinstance(obj, str):
            x = _lit2bv(obj)
            xs.append(x)
        else:
            raise TypeError(f"Invalid input: {obj}")

    return _cat(*xs)


def rep(obj: Bits | int | str, n: int) -> Vector:
    """Repeat a Vector n times."""
    objs = [obj] * n
    return cat(*objs)


def pack(x: Bits | str, n: int = 1) -> Bits:
    """Pack n-bit blocks in right to left order."""
    if n < 1:
        raise ValueError(f"Expected n < 1, got {n}")

    x = _expect_type(x, Bits)
    if x.size % n != 0:
        raise ValueError("Expected x.size to be a multiple of n")

    return _pack(x, n)
