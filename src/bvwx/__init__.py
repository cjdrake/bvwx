"""Bit Vectors With Xes"""

from ._arithmetic import adc, add, div, lsh, mod, mul, neg, ngc, rsh, sbc, srsh, sub
from ._bits import Array, Bits, Empty, Scalar, Vector, bits, i2bv, stack, u2bv
from ._bitwise import and_, impl, ite, mux, nand, nor, not_, or_, xnor, xor
from ._code import decode, encode_onehot, encode_priority
from ._enum import Enum
from ._logical import land, lor, lxor
from ._predicate import eq, ge, gt, le, lt, match, ne, sge, sgt, sle, slt
from ._struct import Struct
from ._unary import uand, uor, uxor
from ._union import Union
from ._word import cat, lrot, pack, rep, rrot, sxt, xt

# Alias Vector to Vec for brevity
Vec = Vector

__all__ = [
    # bits
    "Bits",
    "Empty",
    "Scalar",
    "Vector",
    "Vec",
    "Array",
    "Enum",
    "Struct",
    "Union",
    # bitwise
    "not_",
    "nor",
    "or_",
    "nand",
    "and_",
    "xnor",
    "xor",
    "impl",
    "ite",
    "mux",
    # logical
    "lor",
    "land",
    "lxor",
    # unary
    "uor",
    "uand",
    "uxor",
    # encode/decode
    "encode_onehot",
    "encode_priority",
    "decode",
    # arithmetic
    "add",
    "adc",
    "sub",
    "sbc",
    "neg",
    "ngc",
    "mul",
    "div",
    "mod",
    "lsh",
    "rsh",
    "srsh",
    # word
    "xt",
    "sxt",
    "lrot",
    "rrot",
    "cat",
    "rep",
    "pack",
    # predicate
    "match",
    "eq",
    "ne",
    "lt",
    "le",
    "gt",
    "ge",
    "slt",
    "sle",
    "sgt",
    "sge",
    # factory
    "bits",
    "stack",
    "u2bv",
    "i2bv",
]
