###################
    Quick Start
###################

This chapter will get you started using ``bvwx``.

Install
-------

To install the latest release of BVWX, run:

.. code-block:: console

    $ pip install bvwx

See the :ref:`installation` chapter for more details.

Basic Boolean Algebra
---------------------

Fire up a Python `REPL <https://docs.python.org/3/glossary.html#term-REPL>`_,
ignore the advice given in PEP8's `Imports <https://peps.python.org/pep-0008/#imports>`_ section,
and wildcard-import all names from ``bvwx``:

.. code-block:: python

    >>> from bvwx import *

Create two 4x4 bit arrays ``x0`` and ``x1``, with various known (``0``, ``1``),
and unknown (``-``, ``X``) bit values:

.. code-block:: python

    >>> x0 = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
    >>> x1 = bits(["4b-10X", "4b-10X", "4b-10X", "4b-10X"])
    >>> type(x0)
    bvwx._bits.Array[4,4]
    >>> x0.size
    16
    >>> x0.shape
    (4, 4)

Invoke the Boolean Algebra bitwise operators NOT (``~``), OR (``|``),
AND (``&``), and XOR (``^``) with ``x1`` and ``x2`` as arguments:

.. code-block:: python

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

The multi-dimensional ``Array`` is the most powerful "shaped" data type.
We can perform similar operations on one-dimensional ``Vector``,
zero-dimensional ``Scalar``, and even ``Empty`` bit sequences:

.. code-block:: python

    >>> type(bits("4b0000"))
    bvwx._bits.Vector[4]
    >>> type(bits("1b1"))
    bvwx._bits.Scalar
    >>> type(bits())
    bvwx._bits.Empty

User-Defined Types
------------------

Now that we have experimented with pre-defined data types,
let's create some new ones.
Define a C-style ``Enum``:

.. code-block:: python

    >>> class Color(Enum):
    ...     RED   = "2b00"
    ...     GREEN = "2b01"
    ...     BLUE  = "2b10"
    ...
    >>> type(Color)
    bvwx._enum._EnumMeta
    >>> Color.size
    2

Despite the fancy type definition, enums are just vectors.
Use the ``Color`` values in expressions:

.. code-block:: python

    # Defined values work as expected
    >>> Color.GREEN & Color.BLUE
    Color.RED

    # Undefined values are tolerated
    >>> Color.GREEN | Color.BLUE
    Color("2b11")

Now define a C-style ``Struct``:

.. code-block:: python

    >>> class Pixel(Struct):
    ...     r: Vec[8]
    ...     g: Vec[8]
    ...     b: Vec[8]
    ...
    >>> type(Pixel)
    bvwx._struct._StructMeta
    >>> Pixel.size
    24

Create ``Pixel`` instances, and use them in expressions:

.. code-block:: python

    >>> maize = Pixel(r="8hFF", g="8hCB", b="8h05")
    >>> blue = Pixel(r="8h00", g="8h27", b="8h4C")

    >>> maize & blue
    Pixel(
        r=bits("8b0000_0000"),
        g=bits("8b0000_0011"),
        b=bits("8b0000_0100"),
    )
    >>> maize | blue
    Pixel(
        r=bits("8b1111_1111"),
        g=bits("8b1110_1111"),
        b=bits("8b0100_1101"),
    )

Finally, create a C-style ``Union`` from ``Color`` and ``Pixel`` types:

.. code-block:: python

    >>> class MyUnion(Union):
    ...     c: Color
    ...     p: Pixel
    ...
    >>> type(MyUnion)
    bvwx._union._UnionMeta
    >>> MyUnion.size
    24

Create ``MyUnion`` instances, and use them in expressions:

.. code-block:: python

    >>> u1 = MyUnion(Color.RED)
    >>> u2 = MyUnion(maize)
    >>> u1 | u2
    MyUnion(
        c=Color("2b11"),
        p=Pixel(
            r=bits("8bXXXX_XX11"),
            g=bits("8bXXXX_XXXX"),
            b=bits("8bXXXX_XXXX"),
        ),
    )
