from custom_types import *


class Move(object):

    def __init__(self, yaw: float, radius: float, pitch=0) -> None:
        self.yaw = yaw
        self.radius = radius
        self.pitch = pitch

    def angle_and_radius(self) -> angle_vector3:
        return (self.yaw, self.radius, self.pitch)

    def __str__(self):
        return f"yaw: {self.yaw}, radius: {self.radius}, pitch: {self.pitch}"
