.. _overview:

################
    Overview
################

BVWX (pronounced bih-vuh-wax, like "bivouacs") is a Python library that
implements a family of hardware-oriented bit vector data types and operators.

In this chapter, we will explain what hardware-oriented data types are,
why they are necessary,
and the tradeoffs BVWX makes to model them efficiently.


Logic Design Abstractions
=========================

.. epigraph::

    "We are analog beings living in a digital world,
    facing a quantum future.""

    -- Neil Turok

Designing hardware is different than software in myriad ways.
For example, a hardware description language (HDL) such as `SystemVerilog`_ has
syntax and grammar similar to C, but the semantics are wildly different.
BVWX started as a submodule of the `seqlogic`_ experimental Meta-HDL project,
but the author has since extracted it into a separate library.
It is NOT a full HDL.
Rather, it provides tools for defining and manipulating HDL variables.

Software programming languages like C and Python empower you to create abstract
data types starting from primitives like ``int``, and ``float``.
Looking below their surface,
these primitives are register-aligned, fixed-size sequences of bits (zeros and ones).

HDL variables are different than software variables in two important ways:

* Values are not always fully *known*.
* Storage is bit-aligned.

Beyond Zeros and Ones
---------------------

.. epigraph::

    "... as we know, there are known knowns; there are things we know we know.
    We also know there are known unknowns;
    that is to say we know there are some things we do not know.
    But there are also unknown unknowns—the ones we don't know we don't know."

    -- Donald Rumsfeld

Dive down a few layers of abstraction from software data types to registers
to semiconductor device physics,
and deterministic information dissolves into analog signals and quantum uncertainty.
To grapple with this,
most HDLs provide uninitialized, unspecified, undriven, or uncertain values.
For example, `VHDL`_ uses `Std_logic_1164`_.

BVWX implements a four-state logic:

* ``0`` - False
* ``1`` - True
* ``W`` - Weak Unknown, either True or False, propagates *optimistically*
* ``X`` - Strong Unknown: neither True nor False, propagates *pessimistically*

.. note:: Though four-state logic consists of *quaternary* digits---not
    technically *binary* digits---we will continue referring to them as "bits"
    instead of fabricating a neologism such as "qits".

This system is similar to `SystemVerilog`_'s four-state {0, 1, X, Z} logic,
but with two differences:

* Get rid of Z "high impedance".
* Provide more control over unknown propagation by splitting X into
  weak (``W``) and strong (``X``) versions.

The following table summarizes basic Boolean algebra operators with
{``0``, ``1``, ``W``, ``X``}:

=======  =======  =======  ========  =========  =========
   A        B      NOT A    A OR B    A AND B    A XOR B
=======  =======  =======  ========  =========  =========
 ``0``    ``0``    ``1``    ``0``      ``0``      ``0``
 ``0``    ``1``             ``1``      ``0``      ``1``
 ``1``    ``0``    ``0``    ``1``      ``0``      ``1``
 ``1``    ``1``             ``1``      ``1``      ``0``

 ``W``    ``0``    ``W``    ``W``      ``0``      ``W``
 ``W``    ``1``             ``1``      ``W``      ``W``
 ``W``    ``W``             ``W``      ``W``      ``W``

 ``X``    ``0``    ``X``    ``X``      ``X``      ``X``
 ``X``    ``1``             ``X``      ``X``      ``X``
 ``X``    ``W``             ``X``      ``X``      ``X``
 ``X``    ``X``             ``X``      ``X``      ``X``
=======  =======  =======  ========  =========  =========

The objective is to retain the designer's ability to specify ``W`` "don't care"
values for logic synthesis quality of results (QoR),
while improving debug capabilities with ``X`` pessimism.

See `Improving Verilog Four State Logic <https://cjdrake.substack.com/p/improving-verilog-four-state-logic>`_
for a more thorough explanation of the differences.

All Sizes, Shapes, and Composition
----------------------------------

Software primitives come in fixed bundles such as 32 or 64 bits.
These bundle sizes correspond to the width of architected registers.
Furthermore, they are always aligned with byte-aligned, addressable memory.

Hardware primitives, on the other hand, correspond to flip flops and wires.
They are bit-aligned, not byte/register-aligned.
Overfitting of variable storage (i.e. fewer bits of information than physical storage)
leads to wasted energy through leakage and capacitive discharge,
and therefore shorter battery life.
From a one-bit ``valid`` indicator to a network packet consisting of hundreds
of bytes of header and data fields,
we must be able to precisely specify variable size, shape, composition, and semantics.

The following diagram shows the BVWX family of data types::

                             Bits
                               |
               +---------------+---------------+
               |                               |
            Shaped                         Composite
               |                               |
      +--------+--------+-------+         +----+----+
      |        |        |       |         |         |
    Array > Vector > Scalar > Empty    Struct     Union
               |
             Enum

The base class for all variables is ``Bits``.
A ``Bits`` object is an arbitrary-sized sequence of {``0``, ``1``, ``W``, ``X``} values.
Shaped subclasses (``Empty``, ``Scalar``, ``Vector``, ``Array``, ``Enum``)
have a ``shape`` attribute.
Composite subclasses (``Struct``, ``Union``) have user-defined attributes.

Multi-dimensional arrays allow you to organize information into any size and shape imaginable,
and pack the data into exactly the required number of bits.
C-style ``Enum``, ``Struct``, and ``Union`` allow you to create abstract data
types of arbitrary complexity.


Operator Performance
====================

Hardware designs undergo extensive simulation to verify correctness prior to manufacturing.
Simulation of a digital system is compute intensive,
and modern CPUs do not natively support four-state logic.
For that reason,
when there is a tradeoff between performance and accuracy with respect to
``W`` / ``X`` propagation, BVWX will always choose performance,
preferring algorithms with constant time complexity.

For example,
the ``add`` operator uses Python's integer addition.
It does NOT implement a ripple carry adder to calculate the result bit-by-bit.
When provided inputs that contain ``W``,
it will not attempt to calculate the bit-accurate, "correct" answer.
It will instead return all ``W``:

.. code-block:: python

    >>> add("4b-000", "4b-000")
    bits("4b----")

It is still *possible* to implement bit-accurate ``W`` / ``X`` propagation,
but that is an exercise left to the user.


Summary
=======

To summarize,
BVWX aims to efficiently implement hardware-oriented data types and operators.
This means prioritizing (in no particular order):

* Synthesis QoR
* Debuggability
* Simulation performance
* Abstraction

Four-state logic, bit-aligned data structures, C-style enum/struct/union,
and constant-time operators give hardware design and verification engineers
a useful set of tools for a difficult job.


.. _Espresso: https://ptolemy.berkeley.edu/projects/embedded/pubs/downloads/espresso
.. _Systemverilog: https://standards.ieee.org/ieee/1800/7743
.. _VHDL: https://standards.ieee.org/ieee/1076/3666/
.. _Std_logic_1164: https://standards.ieee.org/ieee/1164/1767/
.. _seqlogic: https://github.com/cjdrake/seqlogic
