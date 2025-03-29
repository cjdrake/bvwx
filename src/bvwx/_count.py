"""Counting"""

from ._bits import BitsLike, Vector, expect_bits
from ._util import clog2, mask


def cpop(x: BitsLike) -> Vector:
    """Count population: return number of set bits."""
    x = expect_bits(x)

    n = clog2(x.size + 1)
    vec = Vector[n]

    if x.has_x():
        return vec.xes()
    if x.has_dc():
        return vec.dcs()

    d1 = x.data[1].bit_count()
    return vec(d1 ^ mask(n), d1)


def clz(x: BitsLike) -> Vector:
    """Count leading zeros."""
    x = expect_bits(x)

    n = clog2(x.size + 1)
    vec = Vector[n]

    if x.has_x():
        return vec.xes()
    if x.has_dc():
        return vec.dcs()

    d1 = x.size - clog2(x.data[1] + 1)
    return vec(d1 ^ mask(n), d1)


def ctz(x: BitsLike) -> Vector:
    """Count trailing zeros."""
    x = expect_bits(x)

    n = clog2(x.size + 1)
    vec = Vector[n]

    if x.has_x():
        return vec.xes()
    if x.has_dc():
        return vec.dcs()

    d = (1 << x.size) - x.data[1]
    d1 = clog2(-d & d)
    return vec(d1 ^ mask(n), d1)
