.. _release_notes:

#####################
    Release Notes
#####################

This chapter lists new features, API changes, and bug fixes.
For a complete history, see the Git commit log.


Version 0.14.0
==============

* Changed ``Bits.has_0`` from method to property
* Changed ``Bits.has_1`` from method to property
* Changed ``Bits.has_x`` from method to property
* Changed ``Bits.has_dc`` from method to property
* Added ``Bits.has_w`` and ``Bits.has_wx`` properties


Version 0.13.0
==============

Updated class inheritance of ``Array``, ``Vector``, ``Scalar``, and ``Empty``.
Now ``Array`` is a subclass of ``Bits``,
``Vector`` is a subclass of ``Array``,
``Scalar`` and ``Empty`` are subclasses of ``Vector``.

For example::

    >>> from bvwx import *
    >>> x = bits("1b1")
    >>> type(x)
    bvwx._bits.Scalar
    >>> isinstance(x, Array)
    True
    >>> isinstance(x, Vector)
    True
    >>> isinstance(x, Scalar)
    True
    >>> isinstance(x, Vec[4])
    False
    >>> isinstance(x, Vec[1])
    True

Changed the ``matmul`` operator so it only works for ``Array`` instances.
It didn't make any sense for ``Composite`` instances.

Added ``Composite`` class to top level namespace.
Consolidated some of the code related to ``Struct`` and ``Union``.

Lots of internal type annotation work.


Version 0.12.0
==============

Updated tooling to use ``uv`` and ``ruff``.


Version 0.11.1
==============

Fixed https://github.com/cjdrake/bvwx/issues/3


Version 0.11.0
==============

Implemented a matrix multiply operator (https://github.com/cjdrake/bvwx/issues/2).


Version 0.10.0
==============

No API changes.

Bug fixes:

* Fixed issue w/ ``Struct`` / ``Union`` string representation.
* Sign extend (``sxt``) empty input raises ``TypeError``.

Added quickstart guide to documentation.

Updates to unit tests to improve code and branch coverage.


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
