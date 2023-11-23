# distutils: extra_compile_args=-Wno-unreachable-code
# distutils: sources=binary_vector/src/*
# distutils: include_dirs=binary_vector/inc
import cython

from cython.cimports.binary_vector.binary_vector import BINARY_VECTOR_P, VEC_init, VEC_del, VEC_mod, VEC_add, VEC_mul


@cython.cclass
class Vector:
    @staticmethod
    @cython.cfunc
    def create(ptr: BINARY_VECTOR_P) -> Vector:
        p = Vector()
        p.data = ptr
        return p

    @staticmethod
    def new(x: cython.float, y: cython.float):
        p = Vector()
        p.data = VEC_init(x, y)
        return p

    def init(self, x: cython.float, y: cython.float):
        self.data = VEC_init(x, y)

    @cython.cfunc
    def init_from_point(self, ptr: BINARY_VECTOR_P) -> cython.void:
        self.data = ptr

    def __dealloc__(self):
        if self.data is not cython.NULL:
            print(f"A dealloc")
            VEC_del(self.data)

    def mod(self) -> float:
        if self.data is not cython.NULL:
            return VEC_mod(self.data)
        raise Exception("vector not init")

    def __add__(self, other: Vector) -> Vector:
        return Vector.create(VEC_add(self.data, other.data))

    def __mul__(self, other: Vector) -> float:
        return VEC_mul(self.data, other.data)
