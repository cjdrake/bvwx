"""Encode/Decode Operators"""

# pylint: disable=protected-access

from ._bits import (
    BitsLike,
    Scalar,
    Vector,
    _expect_bits,
    _Scalar0,
    _Scalar1,
    _ScalarW,
    _ScalarX,
    _vec_size,
)
from ._lbool import _W, _1
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
    x = _expect_bits(x)

    n = clog2(x.size)
    vec = Vector[n]

    # X/DC propagation
    if x.has_x():
        return vec.xes()
    if x.has_dc():
        return vec.dcs()

    d1 = x.data[1]
    is_onehot = d1 != 0 and d1 & (d1 - 1) == 0
    if not is_onehot:
        raise ValueError(f"Expected x to be one-hot encoded, got {x}")

    y = clog2(d1)
    return vec(y ^ mask(n), y)


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
    x = _expect_bits(x)

    n = clog2(x.size)
    vec = Vector[n]

    # X propagation
    if x.has_x():
        return vec.xes(), _ScalarX

    # Handle DC
    if x.has_dc():
        for i in range(x.size - 1, -1, -1):
            x_i = x._get_index(i)
            # 0*1{0,1,-}*
            if x_i == _1:
                return vec(i ^ mask(n), i), _Scalar1
            # 0*-{0,1,-}* => DC
            if x_i == _W:
                return vec.dcs(), _ScalarW

        # Not possible to get here
        assert False  # pragma: no cover

    d1 = x.data[1]

    if d1 == 0:
        return vec.dcs(), _Scalar0

    y = clog2(d1 + 1) - 1
    return vec(y ^ mask(n), y), _Scalar1


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
    x = _expect_bits(x)

    # Output has 2^N bits
    n = 1 << x.size
    vec = _vec_size(n)

    # X/DC propagation
    if x.has_x():
        return vec.xes()
    if x.has_dc():
        return vec.dcs()

    d1 = 1 << x.to_uint()
    return vec(d1 ^ mask(n), d1)
