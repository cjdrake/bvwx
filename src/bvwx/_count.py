"""Counting"""

from ._bits import BitsLike, Vector, _expect_bits, u2bv
from ._util import clog2


def cpop(x: BitsLike) -> Vector:
    """Count population: return number of set bits."""
    x = _expect_bits(x)

    n = clog2(x.size + 1)
    vec = Vector[n]

    if x.has_x():
        return vec.xes()
    if x.has_dc():
        return vec.dcs()

    d1 = x.data[1]
    return u2bv(d1.bit_count(), n)


def clz(x: BitsLike) -> Vector:
    """Count leading zeros."""
    x = _expect_bits(x)

    n = clog2(x.size + 1)
    vec = Vector[n]

    if x.has_x():
        return vec.xes()
    if x.has_dc():
        return vec.dcs()

    d1 = x.data[1]
    return u2bv(x.size - clog2(d1 + 1), n)


def ctz(x: BitsLike) -> Vector:
    """Count trailing zeros."""
    x = _expect_bits(x)

    n = clog2(x.size + 1)
    vec = Vector[n]

    if x.has_x():
        return vec.xes()
    if x.has_dc():
        return vec.dcs()

    d1 = (1 << x.size) - x.data[1]
    return u2bv(clog2(-d1 & d1), n)
