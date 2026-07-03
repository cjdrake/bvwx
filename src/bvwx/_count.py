"""Counting"""

from ._bits import Array, ArrayLike, expect_array, vec
from ._util import clog2


def cpop(x: ArrayLike) -> Array:
    """Count population: return number of set bits."""
    x = expect_array(x)

    n = clog2(x.size + 1)
    V = vec(n)

    if x.has_x():
        return V.xs()
    if x.has_w():
        return V.ws()

    d1 = x._data[1].bit_count()
    d0 = d1 ^ V._dmax
    return V(d0, d1)


def clz(x: ArrayLike) -> Array:
    """Count leading zeros."""
    x = expect_array(x)

    n = clog2(x.size + 1)
    V = vec(n)

    if x.has_x():
        return V.xs()
    if x.has_w():
        return V.ws()

    d1 = x.size - clog2(x._data[1] + 1)
    d0 = d1 ^ V._dmax
    return V(d0, d1)


def ctz(x: ArrayLike) -> Array:
    """Count trailing zeros."""
    x = expect_array(x)

    n = clog2(x.size + 1)
    V = vec(n)

    if x.has_x():
        return V.xs()
    if x.has_w():
        return V.ws()

    d = (1 << x.size) - x._data[1]
    d1 = clog2(-d & d)
    d0 = d1 ^ V._dmax
    return V(d0, d1)
