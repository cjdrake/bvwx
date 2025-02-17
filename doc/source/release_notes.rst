*********************
    Release Notes
*********************

This section lists new features, API changes, and bug fixes.
For a complete history, see the Git commit log.

Version 0.9.0
=============

Update ``xt`` and ``sxt`` functions to accept ``Bits`` object for ``n`` arg.

For example

.. code-block:: python

    >>> xt("4b1010", "2b10")
    bits("6b00_1010")
    >>> sxt("4b1010", "2b10")
    bits("4b11_1010")

Version 0.8.0
=============

Added ``cpop``, ``clz`` and ``ctz`` functions.

Version 0.7.0
=============

Removed bitwise ``nand``, ``nor``, and ``xnor`` operators.

Moved ``clog2`` function into ``bvwx`` namespace.

Version 0.6.0
=============

Added ``lit2bv`` function to top level API.

Version 0.5.0
=============

Improved the type annotations.

Now allows ``W`` character to represent DC in string literals.
For example ``bits("4bW10X")``.

Version 0.4.0
=============

Added logical operators: ``lor``, ``land``, and ``lxor``.
Similar to bitwise, but they only take scalar-like inputs.

Removed ``uxnor`` function.

Added some installation docs.

Version 0.3.0
=============

Add initial documentation.
