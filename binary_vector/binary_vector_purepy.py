import math
from typing import NamedTuple


class BINARY_VECTOR_P(NamedTuple):
    x: float
    y: float


def VEC_init(x: float, y: float) -> BINARY_VECTOR_P:
    return BINARY_VECTOR_P(x, y)


def VEC_del(data: BINARY_VECTOR_P) -> None:
    del data


def VEC_mod(a: BINARY_VECTOR_P) -> float:
    return math.sqrt(a.x**2 + a.y**2)


def VEC_add(a: BINARY_VECTOR_P, b: BINARY_VECTOR_P) -> BINARY_VECTOR_P:
    x = a.x+b.x
    y = a.y+b.y
    return BINARY_VECTOR_P(x, y)


def VEC_mul(a: BINARY_VECTOR_P, b: BINARY_VECTOR_P) -> float:
    return a.x * b.x + a.y * b.y
