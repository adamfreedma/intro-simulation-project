from custom_types import *
import numpy as np
from math_functions import vector_from_angle_and_radius

class Move(object):

    def __init__(self, yaw: float, radius: float, pitch=0) -> None:
        self.__yaw = yaw
        self.__radius = radius
        self.pitch = pitch

    def angle_and_radius(self) -> angle_vector3:
        return (self.__yaw, self.__radius, self.pitch)

    def scale_radius(self, factor: float):
        self.__radius *= factor

    def __add__(self, other: 'Move'):
        self_vector3 = vector_from_angle_and_radius(*self.angle_and_radius())
        other_vector3 = vector_from_angle_and_radius(*other.angle_and_radius())
        return Move(*np.add(self_vector3, other_vector3))
    
    def __str__(self):
        return f"yaw: {self.__yaw}, radius: {self.__radius}, pitch: {self.pitch}"
