"""
Vec.py

This file is part of zreaper, which provides a simple 2D vector class.
"""

from typing import Union


class Vec2:
    """
    A 2D vector class
    """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        """
        Initializes a new Vec2 instance.

        Args:
            x (float): The x-coordinate of the vector.
            y (float): The y-coordinate of the vector.
        """
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"

    def __add__(self, other: "Vec2") -> "Vec2":
        """
        Adds two vectors.

        Args:
            other (Vec2): The vector to add.

        Returns:
            Vec2: The resulting vector.
        """
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        """
        Subtracts two vectors.

        Args:
            other (Vec2): The vector to subtract.

        Returns:
            Vec2: The resulting vector.
        """
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[int, float]) -> "Vec2":
        """
        Multiplies the vector by a scalar.

        Args:
            scalar (Union[int, float]): The scalar to multiply.

        Returns:
            Vec2: The resulting vector.
        """
        return Vec2(self.x * scalar, self.y * scalar)

    def magnitude(self) -> float:
        """
        Calculates the magnitude of the vector.

        Returns:
            float: The magnitude of the vector.
        """
        return (self.x**2 + self.y**2) ** 0.5

    def normalize(self) -> "Vec2":
        """
        Normalizes the vector (makes it unit length).

        Returns:
            Vec2: The normalized vector.
        """
        mag = self.magnitude()
        if mag == 0:
            return Vec2()
        return Vec2(self.x / mag, self.y / mag)

    def clamp(self, minX: float, minY: float, maxX: float, maxY: float) -> None:
        """
        Clamps the vector to the given bounds.

        Args:
            minX (float): The minimum x value.
            minY (float): The minimum y value.
            maxX (float): The maximum x value.
            maxY (float): The maximum y value.
        """
        self.x = max(min(self.x, maxX), minX)
        self.y = max(min(self.y, maxY), minY)

    def isWithin(self, minX: float, minY: float, maxX: float, maxY: float) -> bool:
        """
        Checks if the vector is within the given bounds.

        Args:
            minX (float): The minimum x value.
            minY (float): The minimum y value.
            maxX (float): The maximum x value.
            maxY (float): The maximum y value.
        """
        return minX <= self.x <= maxX and minY <= self.y <= maxY


def clamp(vec: Vec2, minX: float, minY: float, maxX: float, maxY: float) -> None:
    """
    Clamps the vector to the given bounds.

    Args:
        vec (Vec2): The vector to clamp.
        minX (float): The minimum x value.
        minY (float): The minimum y value.
        maxX (float): The maximum x value.
        maxY (float): The maximum y value.
    """
    vec.clamp(minX, minY, maxX, maxY)


def isWithin(vec: Vec2, minX: float, minY: float, maxX: float, maxY: float) -> bool:
    """
    Checks if the vector is within the given bounds.
    Args:
        vec (Vec2): The vector to check.
        minX (float): The minimum x value.
        minY (float): The minimum y value.
        maxX (float): The maximum x value.
        maxY (float): The maximum y value.
    """
    return vec.isWithin(minX, minY, maxX, maxY)
