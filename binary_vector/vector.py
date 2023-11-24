# distutils: extra_compile_args=-Wno-unreachable-code
# distutils: include_dirs=binary_vector/inc
# distutils: sources=binary_vector/src/binary_vector.c

import cython
from typing_extensions import Self


if cython.compiled:
    print("Vector compiled, c impl.")
    from cython.cimports.binary_vector.binary_vector import BINARY_VECTOR_P, VEC_init, VEC_del, VEC_mod, VEC_add, VEC_mul
else:
    print("Vector not compiled, pure python impl.")
    from .binary_vector_purepy import BINARY_VECTOR_P, VEC_init, VEC_del, VEC_mod, VEC_add, VEC_mul

# from cython.cimports.binary_vector.binary_vector import BINARY_VECTOR_P, VEC_init, VEC_del, VEC_mod, VEC_add, VEC_mul

@cython.cclass
class Vector:

    data: BINARY_VECTOR_P

    @staticmethod
    @cython.cfunc
    def create(ptr: BINARY_VECTOR_P):
        p = Vector()
        p.data = ptr
        return p

    @staticmethod
    def new(x: cython.float, y: cython.float):
        p = Vector()
        p.data = VEC_init(x, y)
        return p

    def init(self: Self, x: cython.float, y: cython.float):
        self.data = VEC_init(x, y)

    @cython.cfunc
    def init_from_point(self: Self, ptr: BINARY_VECTOR_P) -> cython.void:
        self.data = ptr

    def __dealloc__(self: Self):
        if self.data is not cython.NULL:
            print(f"A dealloc")
            VEC_del(self.data)

    def mod(self: Self) -> float:
        if self.data is not cython.NULL:
            return VEC_mod(self.data)
        raise Exception("vector not init")

    def __add__(self: Self, other: 'Vector') -> 'Vector':
        
        return Vector.create(VEC_add(self.data, other.data))

    def __mul__(self: Self, other: 'Vector') -> float:
        return VEC_mul(self.data, other.data)
