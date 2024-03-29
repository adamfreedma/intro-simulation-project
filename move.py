from custom_types import *
import numpy as np
from math_functions import vector_from_angle_and_radius, angle_and_radius_from_vector


class Move(object):

    def __init__(self, yaw: float, radius: float, pitch: float = 0) -> None:
        """
        Initialize a Move object.

        Parameters:
            yaw (float): The yaw angle in radians.
            radius (float): The radius of the movement.
            pitch (float, optional): The pitch angle in radians. Default is 0.
        """
        self.__yaw = yaw
        self.__radius = radius
        self.__pitch = pitch

    def angle_and_radius(self) -> angle_vector3:
        """
        Returns the angle, radius, and pitch of the object.

        Returns:
            tuple: A tuple containing the angle, radius, and pitch of the object.
        """
        return (self.__yaw, self.__radius, self.__pitch)

    def scale_radius(self, factor: float) -> None:
        """
        Scales the radius of the object by the given factor.

        Args:
            factor (float): The scaling factor to apply to the radius.
        """
        self.__radius *= factor

    def __add__(self, other: "Move") -> "Move":
        """
        Adds two Move objects together and returns a new Move object.

        Parameters:
            other (Move): The Move object to be added.

        Returns:
            Move: The resulting Move object after addition.
        """
        self_vector3 = vector_from_angle_and_radius(*self.angle_and_radius())
        other_vector3 = vector_from_angle_and_radius(*other.angle_and_radius())
        return Move(
            *angle_and_radius_from_vector(
                cast_to_vector3(np.add(self_vector3, other_vector3))
            )
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        The returned string includes the current values of the yaw, radius, and pitch attributes.

        Returns:
            str: A string representation of the object.
        """
        return f"yaw: {self.__yaw}, radius: {self.__radius}, pitch: {self.__pitch}"
