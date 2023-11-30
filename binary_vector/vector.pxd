
from .binary_vector cimport BINARY_VECTOR_P

cdef class Vector:
    
    cdef BINARY_VECTOR_P data

    @staticmethod
    cdef create(BINARY_VECTOR_P ptr)

    cdef void init_from_point(self, BINARY_VECTOR_P ptr)

    # @staticmethod
    # def new(float x, float y)

    # def init(self, float x, float y)

    # def __dealloc__(self)

    # def mod(self)

    # def __add__(self, other)

    # def __mul__(self, other)
