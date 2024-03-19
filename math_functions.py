import random
import math
from custom_types import *
import numpy as np
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from move import Move

def random_angle() -> float:
    return random.random() * 2 * math.pi

def normalize(vec: vector3) -> vector3:
    if len(vec) == 0 or np.linalg.norm(vec) == 0: # type: ignore[no-untyped-call]
        return vec
    
    return cast(vector3, np.array(vec) / np.linalg.norm(vec)) # type: ignore[no-untyped-call]

def angle_and_radius_from_vector(vec: vector3) -> vector3:
    radius = np.linalg.norm(vec) # type: ignore[no-untyped-call]
    if radius == 0:
        return (0, 0, 0)
    pitch = math.asin(vec[2] / radius)
    yaw = math.atan2(vec[1], vec[0])
    
    return (yaw, radius, pitch)

def vector_from_angle_and_radius(yaw: float, radius: float, pitch: float) -> vector3:
    z = radius * math.sin(pitch)
    floor_radius = radius * math.cos(pitch)
    x = floor_radius * math.cos(yaw)
    y = floor_radius * math.sin(yaw)

    return (x, y, z)


def add_move(location: vector3, move: 'Move') -> vector3:
    move_vector = vector_from_angle_and_radius(*move.angle_and_radius())
    return cast(vector3, np.add(location, move_vector))


def dist(vec1: vector3, vec2: vector3) -> float:
    return float(np.linalg.norm(np.subtract(vec2, vec1))) # type: ignore[no-untyped-call]
