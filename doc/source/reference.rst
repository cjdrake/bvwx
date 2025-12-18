.. _reference:

#################
    Reference
#################


Data Types
==========

.. autoclass:: bvwx.Array
    :show-inheritance:

    .. py:property:: shape
        :type: tuple[int, ...]

    .. py:property:: size
        :type: int

    .. automethod:: bvwx.Array.cast

    .. automethod:: bvwx.Array.xs
    .. automethod:: bvwx.Array.zeros
    .. automethod:: bvwx.Array.ones
    .. automethod:: bvwx.Array.ws
    .. automethod:: bvwx.Array.rand
    .. automethod:: bvwx.Array.xprop

    .. automethod:: bvwx.Array.reshape
    .. automethod:: bvwx.Array.flatten

    .. automethod:: bvwx.Array.__bool__
    .. automethod:: bvwx.Array.__int__

    .. automethod:: bvwx.Array.to_uint
    .. automethod:: bvwx.Array.to_int

    .. automethod:: bvwx.Array.count_zeros
    .. automethod:: bvwx.Array.count_ones
    .. automethod:: bvwx.Array.count_xs
    .. automethod:: bvwx.Array.count_ws
    .. automethod:: bvwx.Array.count_unknown

    .. automethod:: bvwx.Array.onehot
    .. automethod:: bvwx.Array.onehot0

    .. automethod:: bvwx.Array.has_0
    .. automethod:: bvwx.Array.has_1
    .. automethod:: bvwx.Array.has_x
    .. automethod:: bvwx.Array.has_w
    .. automethod:: bvwx.Array.has_xw
    .. automethod:: bvwx.Array.has_unknown

    .. automethod:: bvwx.Array.vcd_var
    .. automethod:: bvwx.Array.vcd_val

.. autoclass:: bvwx.Vector
    :show-inheritance:

.. autoclass:: bvwx.Scalar
    :show-inheritance:

.. autoclass:: bvwx.Empty
    :show-inheritance:

.. autoclass:: bvwx.Enum
    :show-inheritance:

    .. py:property:: name
        :type: str

.. autoclass:: bvwx.Struct
    :show-inheritance:

.. autoclass:: bvwx.Union
    :show-inheritance:


Operators
=========

Bitwise
-------

.. autofunction:: bvwx.not_
.. autofunction:: bvwx.or_
.. autofunction:: bvwx.and_
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
.. autofunction:: bvwx.matmul
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

Count
-----

.. autofunction:: bvwx.cpop
.. autofunction:: bvwx.clz
.. autofunction:: bvwx.ctz


Factory Functions
=================

.. autofunction:: bvwx.bits
.. autofunction:: bvwx.stack
.. autofunction:: bvwx.lit2bv
.. autofunction:: bvwx.u2bv
.. autofunction:: bvwx.i2bv
