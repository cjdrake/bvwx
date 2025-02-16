#################
    Reference
#################

Data Types
==========

.. autoclass:: bvwx.Bits

    .. py:property:: size

        Number of bits

    .. automethod:: bvwx.Bits.cast

    .. automethod:: bvwx.Bits.xes
    .. automethod:: bvwx.Bits.zeros
    .. automethod:: bvwx.Bits.ones
    .. automethod:: bvwx.Bits.dcs

    .. automethod:: bvwx.Bits.xprop

    .. autoproperty:: bvwx.Bits.data

    .. automethod:: bvwx.Bits.__bool__
    .. automethod:: bvwx.Bits.__int__

    .. automethod:: bvwx.Bits.to_uint
    .. automethod:: bvwx.Bits.to_int

    .. automethod:: bvwx.Bits.count_xes
    .. automethod:: bvwx.Bits.count_zeros
    .. automethod:: bvwx.Bits.count_ones
    .. automethod:: bvwx.Bits.count_dcs
    .. automethod:: bvwx.Bits.count_unknown

    .. automethod:: bvwx.Bits.onehot
    .. automethod:: bvwx.Bits.onehot0

    .. automethod:: bvwx.Bits.has_x
    .. automethod:: bvwx.Bits.has_dc
    .. automethod:: bvwx.Bits.has_unknown

.. autoclass:: bvwx.Empty
.. autoclass:: bvwx.Scalar
.. autoclass:: bvwx.Vector
.. autoclass:: bvwx.Array

.. autoclass:: bvwx.Enum
.. autoclass:: bvwx.Struct
.. autoclass:: bvwx.Union

Operators
=========

Bitwise
-------

.. autofunction:: bvwx.not_
.. autofunction:: bvwx.nor
.. autofunction:: bvwx.or_
.. autofunction:: bvwx.and_
.. autofunction:: bvwx.xnor
.. autofunction:: bvwx.xor
.. autofunction:: bvwx.impl
.. autofunction:: bvwx.ite
.. autofunction:: bvwx.mux

Logical
-------

.. autofunction:: bvwx.lor
.. autofunction:: bvwx.land
.. autofunction:: bvwx.lxor

Unary
-----

.. autofunction:: bvwx.uor
.. autofunction:: bvwx.uand
.. autofunction:: bvwx.uxor

Arithmetic
----------

.. autofunction:: bvwx.add
.. autofunction:: bvwx.adc
.. autofunction:: bvwx.sub
.. autofunction:: bvwx.sbc
.. autofunction:: bvwx.neg
.. autofunction:: bvwx.ngc
.. autofunction:: bvwx.mul
.. autofunction:: bvwx.div
.. autofunction:: bvwx.mod
.. autofunction:: bvwx.lsh
.. autofunction:: bvwx.rsh
.. autofunction:: bvwx.srsh

Encode / Decode
---------------

.. autofunction:: bvwx.encode_onehot
.. autofunction:: bvwx.encode_priority
.. autofunction:: bvwx.decode

Word
----

.. autofunction:: bvwx.xt
.. autofunction:: bvwx.sxt
.. autofunction:: bvwx.lrot
.. autofunction:: bvwx.rrot
.. autofunction:: bvwx.cat
.. autofunction:: bvwx.rep
.. autofunction:: bvwx.pack

Predicate
---------

.. autofunction:: bvwx.eq
.. autofunction:: bvwx.ne

.. autofunction:: bvwx.lt
.. autofunction:: bvwx.le
.. autofunction:: bvwx.gt
.. autofunction:: bvwx.ge

.. autofunction:: bvwx.slt
.. autofunction:: bvwx.sle
.. autofunction:: bvwx.sgt
.. autofunction:: bvwx.sge

.. autofunction:: bvwx.match

Factory Functions
=================

.. autofunction:: bvwx.bits
.. autofunction:: bvwx.stack
.. autofunction:: bvwx.lit2bv
.. autofunction:: bvwx.u2bv
.. autofunction:: bvwx.i2bv
