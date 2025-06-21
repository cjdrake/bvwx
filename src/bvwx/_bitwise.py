"""Bitwise Operators"""

import re

from ._bits import (
    Bits,
    BitsLike,
    ScalarLike,
    _and_,
    _impl_,
    _ite_,
    _mux_,
    _not_,
    _or_,
    _xor_,
    expect_bits,
    expect_bits_size,
    expect_scalar,
    resolve_type,
)


def not_(x: BitsLike) -> Bits:
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
        x: ``Bits`` or string literal.

    Returns:
        ``Bits`` of same type and equal size

    Raises:
        TypeError: ``x0`` is not a valid ``Bits`` object.
        ValueError: Error parsing string literal.
    """
    x = expect_bits(x)
    return _not_(x)


def or_(x0: BitsLike, *xs: BitsLike) -> Bits:
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
        x0: ``Bits`` or string literal.
        xs: Sequence of ``Bits`` equal size to ``x0``.

    Returns:
        ``Bits`` equal size to ``x0``.

    Raises:
        TypeError: ``x0`` is not a valid ``Bits`` object,
                   or ``xs[i]`` not equal size to ``x0``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_bits(x0)
    y = x0
    for x in xs:
        y = _or_(y, expect_bits_size(x, x0.size))
    return y


def and_(x0: BitsLike, *xs: BitsLike) -> Bits:
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
        x0: ``Bits`` or string literal.
        xs: Sequence of ``Bits`` equal size to ``x0``.

    Returns:
        ``Bits`` equal size to ``x0``.

    Raises:
        TypeError: ``x0`` is not a valid ``Bits`` object,
                   or ``xs[i]`` not equal size to ``x0``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_bits(x0)
    y = x0
    for x in xs:
        y = _and_(y, expect_bits_size(x, x0.size))
    return y


def xor(x0: BitsLike, *xs: BitsLike) -> Bits:
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
        x0: ``Bits`` or string literal.
        xs: Sequence of ``Bits`` equal size to ``x0``.

    Returns:
        ``Bits`` equal size to ``x0``.

    Raises:
        TypeError: ``x0`` is not a valid ``Bits`` object,
                   or ``xs[i]`` not equal size to ``x0``.
        ValueError: Error parsing string literal.
    """
    x0 = expect_bits(x0)
    y = x0
    for x in xs:
        y = _xor_(y, expect_bits_size(x, x0.size))
    return y


def impl(p: BitsLike, q: BitsLike) -> Bits:
    """Binary bitwise logical IMPL (implies) operator.

    Perform logical IMPL on each bit of the inputs:

    Functionally equivalent to ``~p | q``.

    For example:

    >>> impl("16b----_1111_0000_XXXX", "16b-10X_-10X_-10X_-10X")
    bits("16b-1-X_-10X_111X_XXXX")

    Args:
        p: ``Bits`` or string literal.
        q: ``Bits`` equal size to ``p``.

    Returns:
        ``Bits`` equal size to ``p``.

    Raises:
        TypeError: ``p`` is not a valid ``Bits`` object,
                   or ``q`` not equal size to ``p``.
        ValueError: Error parsing string literal.
    """
    p = expect_bits(p)
    q = expect_bits_size(q, p.size)
    return _impl_(p, q)


def ite(s: ScalarLike, x1: BitsLike, x0: BitsLike) -> Bits:
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
        s: ``Bits`` select
        x1: ``Bits`` or string literal.
        x0: ``Bits`` or string literal equal size to ``x1``.

    Returns:
        ``Bits`` equal size to ``x1``.

    Raises:
        TypeError: ``s`` or ``x1`` are not valid ``Bits`` objects,
                   or ``x0`` not equal size to ``x1``.
        ValueError: Error parsing string literal.
    """
    s = expect_scalar(s)
    x1 = expect_bits(x1)
    x0 = expect_bits_size(x0, x1.size)
    return _ite_(s, x1, x0)


_MUX_XN_RE = re.compile(r"x(\d+)")


def mux(s: BitsLike, **xs: BitsLike) -> Bits:
    r"""Bitwise logical multiplex (mux) operator.

    Args:
        s: ``Bits`` select.
        xs: ``Bits`` or string literal, all equal size.

    Mux input names are in the form xN,
    where N is a valid int.
    Muxes require at least one input.
    Any inputs not specified will default to "don't care".

    For example:

    >>> mux("2b00", x0="4b0001", x1="4b0010", x2="4b0100", x3="4b1000")
    bits("4b0001")
    >>> mux("2b10", x0="4b0001", x1="4b0010", x2="4b0100", x3="4b1000")
    bits("4b0100")

    Handles X and DC propagation:

    >>> mux("2b1-", x0="4b0001", x1="4b0010", x2="4b0100", x3="4b1000")
    bits("4b--00")
    >>> mux("2b1X", x0="4b0001", x1="4b0010", x2="4b0100", x3="4b1000")
    bits("4bXXXX")

    Returns:
        ``Bits`` equal size to ``xN`` inputs.

    Raises:
        TypeError: ``s`` or ``xN`` are not valid ``Bits`` objects,
                   or ``xN`` mismatching size.
        ValueError: Error parsing string literal.
    """
    s = expect_bits(s)
    n = 1 << s.size

    # Parse and check inputs
    t = None
    i2x: dict[int, Bits] = {}
    for name, value in xs.items():
        if m := _MUX_XN_RE.match(name):
            i = int(m.group(1))
            if not 0 <= i < n:
                raise ValueError(f"Expected x in [x0, ..., x{n - 1}]; got {name}")
            if t is None:
                x = expect_bits(value)
                t = type(x)
            else:
                x = expect_bits_size(value, t.size)
                t = resolve_type(t, type(x))
            i2x[i] = x
        else:
            raise ValueError(f"Invalid input name: {name}")

    if t is None:
        raise ValueError("Expected at least one mux input")

    return _mux_(s, t, i2x)
