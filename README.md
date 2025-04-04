# Bit Vectors With Xes

BVWX (pronounced bih-vuh-wax, like "bivouacs") is a Python library that
implements a family of hardware-oriented, bit vector data types and operators.

[Read the docs!](https://bvwx.rtfd.org) (WIP)

[![Documentation Status](https://readthedocs.org/projects/bvwx/badge/?version=latest)](https://bvwx.readthedocs.io/en/latest/?badge=latest)

## Features

The fundamental BVWX data type is an ordered collection of "bits" (i.e. binary digits).
Unlike standard Boolean Algebra where bit values are restricted to {``0``, ``1``},
BVWX extends this to include hardware-oriented values ``DC`` (don't care), and ``X``.

This lifted, four-state logic consists of:

* ``0`` - False
* ``1`` - True
* ``DC`` - Weak Unknown: either True or False, propagates *optimistically*
* ``X`` - Strong Unknown: neither True nor False, propagates *pessimistically*

``DC`` values are denoted by ``-`` or ``W`` in string literals.
The ``-`` character is a convention from the [Espresso][1] PLA file format.
Wherever it hampers readability, we will instead use ``W``.

Collections of bits can be organized into arbitrary shapes using the
multi-dimensional ``Array`` and one-dimensional ``Vec`` class factories.

``Enum``, ``Struct``, and ``Union`` class factories can be extended to create
user-defined abstract date types.

## Example

```python
>>> from bvwx import *

>>> x0 = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
>>> x1 = bits(["4b-10X", "4b-10X", "4b-10X", "4b-10X"])

>>> # Bitwise Operators
>>> ~x0
bits(["4b----", "4b0000", "4b1111", "4bXXXX"])
>>> ~x1
bits(["4b-01X", "4b-01X", "4b-01X", "4b-01X"])
>>> x0 | x1
bits(["4b-1-X", "4b111X", "4b-10X", "4bXXXX"])
>>> x0 & x1
bits(["4b--0X", "4b-10X", "4b000X", "4bXXXX"])
>>> x0 ^ x1
bits(["4b---X", "4b-01X", "4b-10X", "4bXXXX"])

>>> # Enums
>>> class Color(Enum):
...     RED   = "2b00"
...     GREEN = "2b01"
...     BLUE  = "2b10"
...
>>> Color.GREEN & Color.BLUE
Color.RED

>>> # Structs
>>> class Pixel(Struct):
...     r: Vec[8]
...     g: Vec[8]
...     b: Vec[8]
...
>>> maize = Pixel(r="8hFF", g="8hCB", b="8h05")
>>> blue = Pixel(r="8h00", g="8h27", b="8h4C")
>>> maize & blue
Pixel(
    r=bits("8b0000_0000"),
    g=bits("8b0000_0011"),
    b=bits("8b0000_0100"),
)

>>> # And much more ...
```

## Installing

BVWX is available on [PyPI](https://pypi.org):

    $ pip install bvwx

It requires Python 3.12+

## Developing

BVWX's repository is on [GitHub](https://github.com):

    $ git clone https://github.com/cjdrake/bvwx.git

It is 100% Python, and has no runtime dependencies.
Development dependencies are listed in `requirements-dev.txt`.


[//]: Links:

[1]: https://ptolemy.berkeley.edu/projects/embedded/pubs/downloads/espresso
