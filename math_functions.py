import random
import math
from custom_types import *
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from move import Move

def random_angle() -> float:
    """
    Generate a random angle between 0 and 2pi.

    Returns:
        float: A random angle between 0 and 2pi.
    """
    return random.random() * 2 * math.pi

def normalize(vec: vector3) -> vector3:
    """
    Normalize a 3D vector.

    Args:
        vec (vector3): The input vector to be normalized.

    Returns:
        vector3: The normalized vector.

    """
    if len(vec) == 0 or np.linalg.norm(vec) == 0: # type: ignore[no-untyped-call]
        return vec
    # casting back to a vector3
    return cast_to_vector3(np.array(vec) / np.linalg.norm(vec)) # type: ignore[no-untyped-call]

def angle_and_radius_from_vector(vec: vector3) -> vector3:
    """
    Calculates the angle and radius from a given vector.

    Args:
        vec (vector3): The input vector.

    Returns:
        vector3: A tuple containing the yaw, radius, and pitch values.
    """
    radius = np.linalg.norm(vec) # type: ignore[no-untyped-call]
    if radius == 0:
        return (0, 0, 0)
    pitch = math.asin(vec[2] / radius)
    yaw = math.atan2(vec[1], vec[0])
    
    return (yaw, radius, pitch)

def vector_from_angle_and_radius(yaw: float, radius: float, pitch: float) -> vector3:
    """
    Calculates a 3D vector from the given yaw, radius, and pitch values.

    Args:
        yaw (float): The yaw angle in radians.
        radius (float): The radius of the vector.
        pitch (float): The pitch angle in radians.

    Returns:
        vector3: A tuple representing the 3D vector (x, y, z).
    """
    z = radius * math.sin(pitch)
    floor_radius = radius * math.cos(pitch)
    x = floor_radius * math.cos(yaw)
    y = floor_radius * math.sin(yaw)

    return (x, y, z)


def add_move(location: vector3, move: 'Move') -> vector3:
    """
    Adds a move to a location (vector3).

    Args:
        location (vector3): The location.
        move (Move): The move to be added.

    Returns:
        vector3: The new location after adding the move.
    """
    move_vector = vector_from_angle_and_radius(*move.angle_and_radius())
    return cast_to_vector3(np.add(location, move_vector))


def dist(vec1: vector3, vec2: vector3) -> float:
    """
    Calculate the Euclidean distance between two 3D vectors.

    Args:
        vec1 (vector3): The first 3D vector.
        vec2 (vector3): The second 3D vector.

    Returns:
        float: The Euclidean distance between the two vectors.
    """
    return float(np.linalg.norm(np.subtract(vec2, vec1))) # type: ignore[no-untyped-call]
