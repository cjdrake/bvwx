"""Bitwise Operators"""

import re

from . import _lbool as lb
from ._bits import (
    Array,
    ArrayLike,
    ScalarLike,
    Vector,
    bits_and,
    bits_not,
    bits_or,
    bits_xor,
    expect_array,
    expect_array_size,
    expect_scalar,
    resolve_type,
)
from ._util import mask


def not_(x: ArrayLike) -> Array:
    """Unary bitwise logical NOT operator.

    Perform logical negation on each bit of the input:

    +-------+--------+
    |   x   | NOT(x) |
    +=======+========+
    | ``0`` |  ``1`` |
    +-------+--------+
    | ``1`` |  ``0`` |
    +-------+--------+
    | ``X`` |  ``X`` |
    +-------+--------+
    | ``-`` |  ``-`` |
    +-------+--------+

    For example:

    >>> not_("4b-10X")
    bits("4b-01X")

    In expressions, you can use the unary ``~`` operator:

    >>> from bvwx import bits
    >>> a = bits("4b-10X")
    >>> ~a
    bits("4b-01X")

    Args:
        x: ``Array`` or string literal.

    Returns:
        ``Array`` of same type and equal size

    Raises:
        TypeError: ``x0`` is not a valid ``Array`` object.
        ValueError: Error parsing string literal.
    """
    x = expect_array(x)
    return bits_not(x)


def or_(x0: ArrayLike, *xs: ArrayLike) -> Array:
    """N-ary bitwise logical OR operator.

    Perform logical OR on each bit of the inputs:

    +-------+-----------------------+------------+-----------------------+
    |   x0  |           x1          | OR(x0, x1) |          Note         |
    +=======+=======================+============+=======================+
    | ``0`` |                 ``0`` |      ``0`` |                       |
    +-------+-----------------------+------------+-----------------------+
    | ``0`` |                 ``1`` |      ``1`` |                       |
    +-------+-----------------------+------------+-----------------------+
    | ``1`` |                 ``0`` |      ``1`` |                       |
    +-------+-----------------------+------------+-----------------------+
    | ``1`` |                 ``1`` |      ``1`` |                       |
    +-------+-----------------------+------------+-----------------------+
    | ``X`` | {``0``, ``1``, ``-``} |      ``X`` |  ``X`` dominates all  |
    +-------+-----------------------+------------+-----------------------+
    | ``1`` |                 ``-`` |      ``1`` | ``1`` dominates ``-`` |
    +-------+-----------------------+------------+-----------------------+
    | ``-`` |        {``0``, ``-``} |      ``-`` | ``-`` dominates ``0`` |
    +-------+-----------------------+------------+-----------------------+

    For example:

    >>> or_("16b----_1111_0000_XXXX", "16b-10X_-10X_-10X_-10X")
    bits("16b-1-X_111X_-10X_XXXX")

    In expressions, you can use the binary ``|`` operator:

    >>> from bvwx import bits
    >>> a = bits("16b----_1111_0000_XXXX")
    >>> b = bits("16b-10X_-10X_-10X_-10X")
    >>> a | b
    bits("16b-1-X_111X_-10X_XXXX")

    Args:
        x0: ``Array`` or string literal.
        xs: Sequence of ``Array`` equal size to ``x0``.

    Returns:
        ``Array`` equal size to ``x0``.

    Raises:
        TypeError: ``x0`` is not a valid ``Array`` object,
                   or ``xs[i]`` not equal size to ``x0``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    y = x0
    for x in xs:
        y = bits_or(y, expect_array_size(x, x0.size))
    return y


def and_(x0: ArrayLike, *xs: ArrayLike) -> Array:
    """N-ary bitwise logical AND operator.

    Perform logical AND on each bit of the inputs:

    +-------+-----------------------+-------------+-----------------------+
    |   x0  |           x1          | AND(x0, x1) |          Note         |
    +=======+=======================+=============+=======================+
    | ``0`` |                 ``0`` |       ``0`` |                       |
    +-------+-----------------------+-------------+-----------------------+
    | ``0`` |                 ``1`` |       ``0`` |                       |
    +-------+-----------------------+-------------+-----------------------+
    | ``1`` |                 ``0`` |       ``0`` |                       |
    +-------+-----------------------+-------------+-----------------------+
    | ``1`` |                 ``1`` |       ``1`` |                       |
    +-------+-----------------------+-------------+-----------------------+
    | ``X`` | {``0``, ``1``, ``-``} |       ``X`` |  ``X`` dominates all  |
    +-------+-----------------------+-------------+-----------------------+
    | ``0`` |                 ``-`` |       ``0`` | ``0`` dominates ``-`` |
    +-------+-----------------------+-------------+-----------------------+
    | ``-`` |        {``1``, ``-``} |       ``-`` | ``-`` dominates ``1`` |
    +-------+-----------------------+-------------+-----------------------+

    For example:

    >>> and_("16b----_1111_0000_XXXX", "16b-10X_-10X_-10X_-10X")
    bits("16b--0X_-10X_000X_XXXX")

    In expressions, you can use the binary ``&`` operator:

    >>> from bvwx import bits
    >>> a = bits("16b----_1111_0000_XXXX")
    >>> b = bits("16b-10X_-10X_-10X_-10X")
    >>> a & b
    bits("16b--0X_-10X_000X_XXXX")

    Args:
        x0: ``Array`` or string literal.
        xs: Sequence of ``Array`` equal size to ``x0``.

    Returns:
        ``Array`` equal size to ``x0``.

    Raises:
        TypeError: ``x0`` is not a valid ``Array`` object,
                   or ``xs[i]`` not equal size to ``x0``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    y = x0
    for x in xs:
        y = bits_and(y, expect_array_size(x, x0.size))
    return y


def xor(x0: ArrayLike, *xs: ArrayLike) -> Array:
    """N-ary bitwise logical XOR operator.

    Perform logical XOR on each bit of the inputs:

    +-------+-----------------------+-------------+-----------------------+
    |   x0  |           x1          | XOR(x0, x1) |          Note         |
    +=======+=======================+=============+=======================+
    | ``0`` |                 ``0`` |       ``0`` |                       |
    +-------+-----------------------+-------------+-----------------------+
    | ``0`` |                 ``1`` |       ``1`` |                       |
    +-------+-----------------------+-------------+-----------------------+
    | ``1`` |                 ``0`` |       ``1`` |                       |
    +-------+-----------------------+-------------+-----------------------+
    | ``1`` |                 ``1`` |       ``0`` |                       |
    +-------+-----------------------+-------------+-----------------------+
    | ``X`` | {``0``, ``1``, ``-``} |       ``X`` |  ``X`` dominates all  |
    +-------+-----------------------+-------------+-----------------------+
    | ``-`` | {``0``, ``1``. ``-``} |       ``-`` | ``-`` dominates known |
    +-------+-----------------------+-------------+-----------------------+

    For example:

    >>> xor("16b----_1111_0000_XXXX", "16b-10X_-10X_-10X_-10X")
    bits("16b---X_-01X_-10X_XXXX")

    In expressions, you can use the binary ``^`` operator:

    >>> from bvwx import bits
    >>> a = bits("16b----_1111_0000_XXXX")
    >>> b = bits("16b-10X_-10X_-10X_-10X")
    >>> a ^ b
    bits("16b---X_-01X_-10X_XXXX")

    Args:
        x0: ``Array`` or string literal.
        xs: Sequence of ``Array`` equal size to ``x0``.

    Returns:
        ``Array`` equal size to ``x0``.

    Raises:
        TypeError: ``x0`` is not a valid ``Array`` object,
                   or ``xs[i]`` not equal size to ``x0``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_array(x0)
    y = x0
    for x in xs:
        y = bits_xor(y, expect_array_size(x, x0.size))
    return y


def _impl[T: Array](p: T, q: Array) -> T | Vector:
    d0, d1 = lb.impl(p.data, q.data)
    t = resolve_type(p, q)
    return t.cast_data(d0, d1)


def impl(p: ArrayLike, q: ArrayLike) -> Array:
    """Binary bitwise logical IMPL (implies) operator.

    Perform logical IMPL on each bit of the inputs:

    Functionally equivalent to ``~p | q``.

    For example:

    >>> impl("16b----_1111_0000_XXXX", "16b-10X_-10X_-10X_-10X")
    bits("16b-1-X_-10X_111X_XXXX")

    Args:
        p: ``Array`` or string literal.
        q: ``Array`` equal size to ``p``.

    Returns:
        ``Array`` equal size to ``p``.

    Raises:
        TypeError: ``p`` is not a valid ``Array`` object,
                   or ``q`` not equal size to ``p``.
        ValueError: Error parsing string literal.
    """
    p = expect_array(p)
    q = expect_array_size(q, p.size)
    return _impl(p, q)


def _ite[T: Array](s: Array, x1: T, x0: Array) -> T | Vector:
    s0 = mask(x1.size) * s.data[0]
    s1 = mask(x1.size) * s.data[1]
    d0, d1 = lb.ite((s0, s1), x1.data, x0.data)
    t = resolve_type(x1, x0)
    return t.cast_data(d0, d1)


def ite(s: ScalarLike, x1: ArrayLike, x0: ArrayLike) -> Array:
    """Ternary bitwise logical if-then-else (ITE) operator.

    Perform logical ITE on each bit of the inputs:

    +-------+-----------------------+-----------------------+----------------+
    |   s   |           x1          |           x0          | ITE(s, x1, x0) |
    +=======+=======================+=======================+================+
    | ``1`` | {``0``, ``1``, ``-``} |                       |         ``x1`` |
    +-------+-----------------------+-----------------------+----------------+
    | ``0`` |                       | {``0``, ``1``, ``-``} |         ``x0`` |
    +-------+-----------------------+-----------------------+----------------+
    | ``X`` |                       |                       |          ``X`` |
    +-------+-----------------------+-----------------------+----------------+
    |       |                 ``X`` |                       |          ``X`` |
    +-------+-----------------------+-----------------------+----------------+
    |       |                       |                 ``X`` |          ``X`` |
    +-------+-----------------------+-----------------------+----------------+
    | ``-`` |                 ``0`` |                 ``0`` |          ``0`` |
    +-------+-----------------------+-----------------------+----------------+
    | ``-`` |                 ``0`` |        {``1``, ``-``} |          ``-`` |
    +-------+-----------------------+-----------------------+----------------+
    | ``-`` |                 ``1`` |                 ``1`` |          ``1`` |
    +-------+-----------------------+-----------------------+----------------+
    | ``-`` |                 ``1`` |        {``0``, ``-``} |          ``-`` |
    +-------+-----------------------+-----------------------+----------------+
    | ``-`` |                 ``-`` | {``0``, ``1``, ``-``} |          ``-`` |
    +-------+-----------------------+-----------------------+----------------+

    For example:

    >>> ite("1b0", "16b----_1111_0000_XXXX", "16b-10X_-10X_-10X_-10X")
    bits("16b-10X_-10X_-10X_XXXX")
    >>> ite("1b1", "16b----_1111_0000_XXXX", "16b-10X_-10X_-10X_-10X")
    bits("16b---X_111X_000X_XXXX")
    >>> ite("1b-", "16b----_1111_0000_XXXX", "16b-10X_-10X_-10X_-10X")
    bits("16b---X_-1-X_--0X_XXXX")

    Args:
        s: ``Array`` select
        x1: ``Array`` or string literal.
        x0: ``Array`` or string literal equal size to ``x1``.

    Returns:
        ``Array`` equal size to ``x1``.

    Raises:
        TypeError: ``s`` or ``x1`` are not valid ``Array`` objects,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    s = expect_scalar(s)
    x1 = expect_array(x1)
    x0 = expect_array_size(x0, x1.size)
    return _ite(s, x1, x0)


def _mux[T: Array](t: type[T], s: Array, xs: dict[int, Array]) -> T:
    m = mask(t.size)
    si = (s.get_index(i) for i in range(s.size))
    _s = tuple((m * d0, m * d1) for d0, d1 in si)
    _xs = {i: x.data for i, x in xs.items()}
    w = t.ws()
    d0, d1 = lb.mux(_s, _xs, w.data)
    return t.cast_data(d0, d1)


_MUX_XN_RE = re.compile(r"x(\d+)")


def mux(s: ArrayLike, **xs: ArrayLike) -> Array:
    r"""Bitwise logical multiplex (mux) operator.

    Args:
        s: ``Array`` select.
        xs: ``Array`` or string literal, all equal size.

    Mux input names are in the form xN,
    where N is a valid int.
    Muxes require at least one input.
    Any inputs not specified will default to "don't care".

    For example:

    >>> mux("2b00", x0="4b0001", x1="4b0010", x2="4b0100", x3="4b1000")
    bits("4b0001")
    >>> mux("2b10", x0="4b0001", x1="4b0010", x2="4b0100", x3="4b1000")
    bits("4b0100")

    Handles X and W propagation:

    >>> mux("2b1-", x0="4b0001", x1="4b0010", x2="4b0100", x3="4b1000")
    bits("4b--00")
    >>> mux("2b1X", x0="4b0001", x1="4b0010", x2="4b0100", x3="4b1000")
    bits("4bXXXX")

    Returns:
        ``Array`` equal size to ``xN`` inputs.

    Raises:
        TypeError: ``s`` or ``xN`` are not valid ``Array`` objects,
                   or ``xN`` mismatching size.
        ValueError: Error parsing string literal.
    """
    _s = expect_array(s)
    n = 1 << _s.size

    # Parse and check inputs
    x0 = None
    t = None
    _xs: dict[int, Array] = {}
    for name, value in xs.items():
        if m := _MUX_XN_RE.match(name):
            i = int(m.group(1))
            if not 0 <= i < n:
                raise ValueError(f"Expected x in [x0, ..., x{n - 1}]; got {name}")
            if x0 is None:
                x = expect_array(value)
                x0, t = x, type(x)
            else:
                x = expect_array_size(value, x0.size)
                t = resolve_type(x0, x)
            _xs[i] = x
        else:
            raise ValueError(f"Invalid input name: {name}")

    if t is None:
        raise ValueError("Expected at least one mux input")

    return _mux(t, _s, _xs)
