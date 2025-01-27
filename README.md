# Bit Vectors With Xes

BVWX (pronounced bih-vuh-wax, like "bivouacs") is a Python library that
implements a family of four-state, hardware-oriented bit vector data types.

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

``DC`` values are denoted by ``-`` in string literals.
This is a convention from the [Espresso][1] PLA file format.
Wherever it hampers readability, we will instead use ``W``.

Collections of bits can be organized into arbitrary shapes using the
multi-dimensional ``Array`` and one-dimensional ``Vec`` class factories.

For abstraction purposes, BVWX also provides user-defined
``Enum``, ``Struct``, and ``Union`` class factories.

## Example

```python
>>> from bvwx import *

>>> # Bitwise Operators
>>> x0 = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
>>> x1 = bits(["4b-10X", "4b-10X", "4b-10X", "4b-10X"])
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

>>> Pixel(r="8h01", g="8h15", b="8h3E")  # navy blue
Pixel(
    r=bits("8b0000_0001"),
    g=bits("8b0001_0101"),
    b=bits("8b0011_1110"),
)

>>> # And much more ...
```

## Installing

BVWX is available on [PyPI](https://pypi.org):

    $ pip install bvwx

It supports Python 3.12+

## Developing

BVWX's repository is on [GitHub](https://github.com):

    $ git clone https://github.com/cjdrake/bvwx.git

It is 100% Python, and has no runtime dependencies.
Development dependencies are listed in `requirements-dev.txt`.


[//]: Links:

[1]: https://ptolemy.berkeley.edu/projects/embedded/pubs/downloads/espresso
