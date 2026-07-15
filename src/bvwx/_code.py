"""Encode/Decode Operators"""

from . import _lbool as lb
from ._bits import (
    Array,
    ArrayLike,
    expect_array,
    scalar0,
    scalar1,
    scalarW,
    scalarX,
    vec,
)
from ._util import clog2


def encode_onehot(x: ArrayLike) -> Array:
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
        x: ``Array`` or string literal.

    Returns:
        ``Vector`` with ``size`` = ``clog2(x.size)``

    Raises:
        TypeError: ``x`` is not a valid ``Array`` object.
        ValueError: ``x`` is not one-hot encoded.
    """
    x = expect_array(x)

    if x.size == 0:
        raise ValueError("Expected non-empty Array")

    n = clog2(x.size)
    V = vec(n)

    # X/W propagation
    if x.has_x():
        return V.xs()
    if x.has_w():
        return V.ws()

    d1 = x._data[1]
    is_onehot = d1 != 0 and d1 & (d1 - 1) == 0
    if not is_onehot:
        raise ValueError(f"Expected x to be one-hot encoded, got {x}")

    y1 = clog2(d1)
    y0 = y1 ^ V._dmax
    return V(y0, y1)


def encode_priority(x: ArrayLike) -> tuple[Array, Array]:
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
        x: ``Array`` or string literal.

    Returns:
        Tuple of ``Vector`` and ``Scalar``:
            ``Vector`` with ``size`` = ``clog2(x.size)``
            ``Scalar`` valid bit

    Raises:
        TypeError: ``x`` is not a valid ``Array`` object.
    """
    x = expect_array(x)

    if x.size == 0:
        raise ValueError("Expected non-empty Array")

    n = clog2(x.size)
    V = vec(n)

    # X propagation
    if x.has_x():
        return V.xs(), scalarX

    # Handle W
    if x.has_w():
        for i in range(x.size - 1, -1, -1):
            x_i = x._get_index(i)
            # 0*1{0,1,-}*
            if x_i == lb.T:
                return V(i ^ V._dmax, i), scalar1
            # 0*-{0,1,-}* => W
            if x_i == lb.W:
                return V.ws(), scalarW

        # Not possible to get here
        assert False  # pragma: no cover

    d1 = x._data[1]

    if d1 == 0:
        return V.ws(), scalar0

    y1 = clog2(d1 + 1) - 1
    y0 = y1 ^ V._dmax
    return V(y0, y1), scalar1


def decode(x: ArrayLike) -> Array:
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
        x: ``Array`` or string literal.

    Returns:
        One hot ``Scalar`` or ``Vector`` with ``size`` = ``2**x.size``

    Raises:
        TypeError: ``x`` is not a valid ``Array`` object.
        ValueError: Error parsing string literal.
    """
    x = expect_array(x)

    # Output has 2^N bits
    n = 1 << x.size
    V = vec(n)

    # X/W propagation
    if x.has_x():
        return V.xs()
    if x.has_w():
        return V.ws()

    d1 = 1 << x.to_uint()
    d0 = d1 ^ V._dmax
    return V(d0, d1)
