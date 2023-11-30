# distutils: language = c++
# distutils: sources = binary_vector/binary_vector.cpp
from .binary_vector cimport BINARY_VECTOR_P, VEC_init, VEC_del, VEC_mod, VEC_add, VEC_mul
from libcpp.string cimport string
from .spdlog cimport info, warn


cdef string warn_msg = b"Vector compiled, c impl."
warn(warn_msg)


cdef class Vector:

    property x:
        def __get__(self):
            return self.data.x
    property y:
        def __get__(self):
            return self.data.y

    @staticmethod
    cdef create(BINARY_VECTOR_P ptr):
        p = Vector()
        p.data = ptr
        return p

    @staticmethod
    def new(x: float, y: float):
        p = Vector()
        p.data = VEC_init(x, y)
        return p

    def init(self, x: float, y: float):
        self.data = VEC_init(x, y)

    cdef void init_from_point(self, BINARY_VECTOR_P ptr):
        self.data = ptr

    def __dealloc__(self):
        if self.data is not NULL:
            msg: string = b"A dealloc"
            info(msg)
            VEC_del(self.data)

    def mod(self) -> float:
        if self.data is not NULL:
            return VEC_mod(self.data)
        raise Exception("vector not init")

    def __add__(self, other: 'Vector') -> 'Vector':

        return Vector.create(VEC_add(self.data, other.data))

    def __mul__(self, other: 'Vector') -> float:
        return VEC_mul(self.data, other.data)
