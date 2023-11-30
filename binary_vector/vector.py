import math
import warnings
from typing_extensions import Self

warn_message = "model vector has cython implement, but now just pure python implement"
warnings.warn(warn_message)


class Vector:

    _x: float
    _y: float

    @property
    def x(self: Self) -> float:
        return self._x

    @property
    def y(self: Self) -> float:
        return self._y

    @staticmethod
    def new(x: float, y: float):
        p = Vector()
        p._x = x
        p._y = y
        return p

    def init(self: Self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    def __init__(self: Self) -> None:
        self._x = 0
        self._y = 0

    def mod(self: Self) -> float:
        return math.sqrt(self._x**2 + self._y**2)

    def __add__(self: Self, other: Self) -> Self:
        x = self._x+other.x
        y = self._y+other.y
        return Vector.new(x, y)

    def __mul__(self: Self, other: Self) -> float:
        return self._x * other.x + self.y * other.y
