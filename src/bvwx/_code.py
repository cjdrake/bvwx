"""Encode/Decode Operators"""

from . import _lbool as lb
from ._bits import (
    BitsLike,
    Scalar,
    Vector,
    expect_bits,
    scalar0,
    scalar1,
    scalarW,
    scalarX,
    vec_size,
)
from ._util import clog2, mask


def encode_onehot(x: BitsLike) -> Vector:
    """Compress one-hot encoding to an index.

    The index is the highest bit set in the input.

    For example:

    >>> encode_onehot("2b01")
    bits("1b0")
    >>> encode_onehot("2b10")
    bits("1b1")
    >>> encode_onehot("3b010")
    bits("2b01")

    Args:
        x: ``Bits`` or string literal.

    Returns:
        ``Vector`` w/ ``size`` = ``clog2(x.size)``

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: ``x`` is not one-hot encoded.
    """
    x = expect_bits(x)

    n = clog2(x.size)
    V = vec_size(n)

    # X/DC propagation
    if x.has_x:
        return V.xes()
    if x.has_dc():
        return V.dcs()

    d1 = x.data[1]
    is_onehot = d1 != 0 and d1 & (d1 - 1) == 0
    if not is_onehot:
        raise ValueError(f"Expected x to be one-hot encoded, got {x}")

    y = clog2(d1)
    return V(y ^ mask(n), y)


def encode_priority(x: BitsLike) -> tuple[Vector, Scalar]:
    """Compress priority encoding to (index, valid) tuple.

    The index is the highest bit set in the input.

    For example:

    >>> encode_priority("2b01")
    (bits("1b0"), bits("1b1"))
    >>> encode_priority("2b10")
    (bits("1b1"), bits("1b1"))
    >>> encode_priority("3b1--")
    (bits("2b10"), bits("1b1"))

    Args:
        x: ``Bits`` or string literal.

    Returns:
        Tuple of ``Vector`` and ``Scalar``:
            ``Vector`` w/ ``size`` = ``clog2(x.size)``
            ``Scalar`` valid bit

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object.
    """
    x = expect_bits(x)

    n = clog2(x.size)
    V = vec_size(n)

    # X propagation
    if x.has_x:
        return V.xes(), scalarX

    # Handle DC
    if x.has_dc():
        for i in range(x.size - 1, -1, -1):
            x_i = x._get_index(i)
            # 0*1{0,1,-}*
            if x_i == lb.T:
                return V(i ^ mask(n), i), scalar1
            # 0*-{0,1,-}* => DC
            if x_i == lb.W:
                return V.dcs(), scalarW

        # Not possible to get here
        assert False  # pragma: no cover

    d1 = x.data[1]

    if d1 == 0:
        return V.dcs(), scalar0

    y = clog2(d1 + 1) - 1
    return V(y ^ mask(n), y), scalar1


def decode(x: BitsLike) -> Vector:
    """Decode dense encoding to sparse, one-hot encoding.

    For example:

    >>> decode("2b00")
    bits("4b0001")
    >>> decode("2b01")
    bits("4b0010")
    >>> decode("2b10")
    bits("4b0100")
    >>> decode("2b11")
    bits("4b1000")

    Empty input returns 1b1:

    >>> from bvwx import bits
    >>> decode(bits())
    bits("1b1")

    Args:
        x: ``Bits`` or string literal.

    Returns:
        One hot ``Scalar`` or ``Vector`` w/ ``size`` = ``2**x.size``

    Raises:
        TypeError: ``x`` is not a valid ``Bits`` object.
        ValueError: Error parsing string literal.
    """
    x = expect_bits(x)

    # Output has 2^N bits
    n = 1 << x.size
    V = vec_size(n)

    # X/DC propagation
    if x.has_x:
        return V.xes()
    if x.has_dc():
        return V.dcs()

    d1 = 1 << x.to_uint()
    return V(d1 ^ mask(n), d1)
