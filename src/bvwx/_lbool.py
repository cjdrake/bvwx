"""Lifted Boolean Data Type and Operators"""

import re

from ._util import mask

# Lifted Boolean Vector
type lbv = tuple[int, int]


# Scalars
_X: lbv = (0, 0)
_0: lbv = (1, 0)
_1: lbv = (0, 1)
_W: lbv = (1, 1)


from_char: dict[str, lbv] = {
    "X": _X,
    "0": _0,
    "1": _1,
    "-": _W,
    "W": _W,
}

to_char: dict[lbv, str] = {
    _X: "X",
    _0: "0",
    _1: "1",
    _W: "-",
}

to_vcd_char: dict[lbv, str] = {
    _X: "x",
    _0: "0",
    _1: "1",
    _W: "x",
}

_LIT_PREFIX_RE = re.compile(r"(?P<Size>[1-9][0-9]*)(?P<Base>[bdh])")


def parse_lit(lit: str) -> tuple[int, lbv]:
    m = _LIT_PREFIX_RE.match(lit)

    if m is None:
        raise ValueError(f"Invalid lit: {lit}")

    size = int(m.group("Size"))
    base: str = m.group("Base")
    prefix_len = len(m.group())
    digits = lit[prefix_len:]

    # Binary
    if base == "b":
        digits = digits.replace("_", "")
        if len(digits) != size:
            s = f"Expected {size} digits, got {len(digits)}"
            raise ValueError(s)
        d0, d1 = 0, 0
        for i, c in enumerate(reversed(digits)):
            try:
                x = from_char[c]
            except KeyError as e:
                raise ValueError(f"Invalid lit: {lit}") from e
            d0 |= x[0] << i
            d1 |= x[1] << i
        return size, (d0, d1)

    # Decimal
    if base == "d":
        d1 = int(digits, base=10)
        dmax = mask(size)
        if d1 > dmax:
            s = f"Expected digits in range [0, {dmax}], got {digits}"
            raise ValueError(s)
        return size, (d1 ^ dmax, d1)

    # Hexadecimal
    if base == "h":
        d1 = int(digits, base=16)
        dmax = mask(size)
        if d1 > dmax:
            s = f"Expected digits in range [0, {dmax}], got {digits}"
            raise ValueError(s)
        return size, (d1 ^ dmax, d1)

    assert False  # pragma: no cover


def not_(a: lbv) -> lbv:
    """Lifted NOT."""
    return a[1], a[0]


def or_(a: lbv, b: lbv) -> lbv:
    r"""Lifted OR.

    Karnaugh Map::

            b
          \ 00 01 11 10
           +--+--+--+--+
      a 00 |00|00|00|00|  y1 = a[0] & b[1]
           +--+--+--+--+     | a[1] & b[0]
        01 |00|01|11|10|     | a[1] & b[1]
           +--+--+--+--+
        11 |00|11|11|10|  y0 = a[0] & b[0]
           +--+--+--+--+
        10 |00|10|10|10|
           +--+--+--+--+
    """
    return (
        a[0] & b[0],
        a[0] & b[1] | a[1] & b[0] | a[1] & b[1],
    )


def and_(a: lbv, b: lbv) -> lbv:
    r"""Lifted AND.

    Karnaugh Map::

            b
          \ 00 01 11 10
           +--+--+--+--+
      a 00 |00|00|00|00|  y1 = a[1] & b[1]
           +--+--+--+--+
        01 |00|01|01|01|
           +--+--+--+--+
        11 |00|01|11|11|  y0 = a[0] & b[0]
           +--+--+--+--+     | a[0] & b[1]
        10 |00|01|11|10|     | a[1] & b[0]
           +--+--+--+--+
    """
    return (
        a[0] & b[0] | a[0] & b[1] | a[1] & b[0],
        a[1] & b[1],
    )


def xnor(a: lbv, b: lbv) -> lbv:
    r"""Lifted XNOR.

    Karnaugh Map::

            b
          \ 00 01 11 10
           +--+--+--+--+
      a 00 |00|00|00|00|  y1 = a[0] & b[0]
           +--+--+--+--+     | a[1] & b[1]
        01 |00|10|11|01|
           +--+--+--+--+
        11 |00|11|11|11|  y0 = a[0] & b[1]
           +--+--+--+--+     | a[1] & b[0]
        10 |00|01|11|10|
           +--+--+--+--+
    """
    return (
        a[0] & b[1] | a[1] & b[0],
        a[0] & b[0] | a[1] & b[1],
    )


def xor(a: lbv, b: lbv) -> lbv:
    r"""Lifted XOR.

    Karnaugh Map::

            b
          \ 00 01 11 10
           +--+--+--+--+
      a 00 |00|00|00|00|  y1 = a[0] & b[1]
           +--+--+--+--+     | a[1] & b[0]
        01 |00|01|11|10|
           +--+--+--+--+
        11 |00|11|11|11|  y0 = a[0] & b[0]
           +--+--+--+--+     | a[1] & b[1]
        10 |00|10|11|01|
           +--+--+--+--+
    """
    return (
        a[0] & b[0] | a[1] & b[1],
        a[0] & b[1] | a[1] & b[0],
    )


def impl(p: lbv, q: lbv) -> lbv:
    r"""Lifted IMPL.

    Karnaugh Map::

             q
           \ 00 01 11 10
            +--+--+--+--+
       p 00 |00|00|00|00|  y1 = p[0] & q[0]
            +--+--+--+--+     | p[0] & q[1]
         01 |00|10|10|10|     | p[1] & q[1]
            +--+--+--+--+
         11 |00|11|11|10|  y0 = p[1] & q[0]
            +--+--+--+--+
         10 |00|01|11|10|
            +--+--+--+--+
    """
    return (
        p[1] & q[0],
        p[0] & q[0] | p[0] & q[1] | p[1] & q[1],
    )


def ite(s: lbv, a: lbv, b: lbv) -> lbv:
    r"""Lifted If-Then-Else.

    Karnaugh Map::

      s=00  b                             s=01  b
          \ 00 01 11 10                       \ 00 01 11 10
           +--+--+--+--+                       +--+--+--+--+
      a 00 |00|00|00|00|                  a 00 |00|00|00|00|  s0 b0 a0
           +--+--+--+--+                       +--+--+--+--+  s0 b0 a1
        01 |00|00|00|00|                    01 |00|01|11|10|
           +--+--+--+--+                       +--+--+--+--+  s0 b1 a0
        11 |00|00|00|00|                    11 |00|01|11|10|  s0 b1 a1
           +--+--+--+--+                       +--+--+--+--+
        10 |00|00|00|00|                    10 |00|01|11|10|
           +--+--+--+--+                       +--+--+--+--+

      s=10  b                             s=11  b
          \ 00 01 11 10                       \ 00 01 11 10
           +--+--+--+--+                       +--+--+--+--+
      a 00 |00|00|00|00|  s1 a0 b0        a 00 |00|00|00|00|
           +--+--+--+--+  s1 a0 b1             +--+--+--+--+
        01 |00|01|01|01|                    01 |00|01|11|11|
           +--+--+--+--+  s1 a1 b0             +--+--+--+--+
        11 |00|11|11|11|  s1 a1 b1          11 |00|11|11|11|
           +--+--+--+--+                       +--+--+--+--+
        10 |00|10|10|10|                    10 |00|11|11|10|
           +--+--+--+--+                       +--+--+--+--+
    """
    a_01 = a[0] | a[1]
    b_01 = b[0] | b[1]
    return (
        s[1] & a[0] & b_01 | s[0] & b[0] & a_01,
        s[1] & a[1] & b_01 | s[0] & b[1] & a_01,
    )


def _mux(s: lbv, x0: lbv, x1: lbv) -> lbv:
    """Lifted 2:1 Mux."""
    x0_01 = x0[0] | x0[1]
    x1_01 = x1[0] | x1[1]
    return (
        s[0] & x0[0] & x1_01 | s[1] & x1[0] & x0_01,
        s[0] & x0[1] & x1_01 | s[1] & x1[1] & x0_01,
    )


def mux(s: tuple[lbv, ...], xs: dict[int, lbv], default: lbv) -> lbv:
    """Lifted N:1 Mux."""
    n = 1 << len(s)

    x0 = default

    if n == 1:
        for i, x in xs.items():
            assert i < n
            x0 = x
        return x0

    x1 = default

    if n == 2:  # noqa: PLR2004
        for i, x in xs.items():
            assert i < n
            if i:
                x1 = x
            else:
                x0 = x
        return _mux(s[0], x0, x1)

    mask0 = (n >> 1) - 1
    xs_0: dict[int, lbv] = {}
    xs_1: dict[int, lbv] = {}
    for i, x in xs.items():
        assert i < n
        if i > mask0:
            xs_1[i & mask0] = x
        else:
            xs_0[i] = x
    if xs_0:
        x0 = mux(s[:-1], xs_0, default)
    if xs_1:
        x1 = mux(s[:-1], xs_1, default)
    return _mux(s[-1], x0, x1)
