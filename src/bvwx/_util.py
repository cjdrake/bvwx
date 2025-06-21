"""Utility functions."""

from math import ceil, log2


def clog2(x: int) -> int:
    """Return the ceiling log base two of an integer ≥ 1.

    Tells you the minimum dimension of a Boolean space with at least N points.

    For example, here are the values of ``clog2(N)`` for :math:`1 ≤ N < 18`:

    >>> [clog2(n) for n in range(1, 18)]
    [0, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5]

    Defined only for positive integers:

    >>> clog2(0)
    Traceback (most recent call last):
        ...
    ValueError: math domain error
    """
    return ceil(log2(x))


def mask(n: int) -> int:
    """Return n bit mask."""
    return (1 << n) - 1
