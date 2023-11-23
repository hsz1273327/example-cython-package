from .binary_vector import BINARY_VECTOR_P
cdef class Vector:
    cdef BINARY_VECTOR_P data

    @staticmethod
    cdef create(BINARY_VECTOR_P ptr)

    cdef void init_from_point(self,BINARY_VECTOR_P ptr)
