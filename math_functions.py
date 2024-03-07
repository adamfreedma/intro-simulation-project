import random
import math
from custom_types import *
from move import Move
import numpy as np


def random_angle() -> float:
    return random.random() * 2 * math.pi

def vector_from_angle_and_radius(yaw: float, radius: float, pitch: float) -> vector3:
    z = radius * math.sin(pitch)
    floor_radius = radius * math.cos(pitch)
    x = floor_radius * math.cos(yaw)
    y = floor_radius * math.sin(yaw)

    return (x, y, z)

def add_move(location: vector3, move: Move) -> vector3:
    move_vector = vector_from_angle_and_radius(*move.angle_and_radius())
    return np.add(location, move_vector)

def dist(vec1: vector3, vec2: vector3) -> float:
    return np.linalg.norm(np.subtract(vec2, vec1))