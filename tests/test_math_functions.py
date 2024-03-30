from math_functions import MathFunctions
import math
from move import Move
from custom_types import *


def test_random_angle() -> None:
    angle = MathFunctions.random_angle()
    assert isinstance(angle, float)
    assert angle >= 0.0 and angle <= 2 * math.pi


def test_normalize() -> None:
    vec = (1.0, 2.0, 3.0)
    normalized_vec = MathFunctions.normalize(vec)
    assert math.isclose(
        math.sqrt(
            normalized_vec[0] ** 2 + normalized_vec[1] ** 2 + normalized_vec[2] ** 2
        ),
        1.0,
    )


def test_angle_and_radius_from_vector() -> None:
    vec = (1.0, 2.0, 3.0)
    angle_radius = MathFunctions.angle_and_radius_from_vector(vec)
    assert len(angle_radius) == 3


def test_vector_from_angle_and_radius() -> None:
    yaw = 45.0
    radius = 1.0
    pitch = 30.0
    vec = MathFunctions.vector_from_angle_and_radius(yaw, radius, pitch)
    assert len(vec) == 3


def test_add_move() -> None:
    location = (1.0, 2.0, 3.0)
    new_location = MathFunctions.add_move(
        location, Move(*MathFunctions.angle_and_radius_from_vector(location))
    )
    assert math.isclose(new_location[0], location[0] * 2)
    assert math.isclose(new_location[1], location[1] * 2)
    assert math.isclose(new_location[2], location[2] * 2)


def test_dist() -> None:
    vec1 = (1.0, 2.0, 3.0)
    vec2 = (4.0, 5.0, 6.0)
    distance = MathFunctions.dist(vec1, vec2)
    assert isinstance(distance, float)
    assert distance == math.sqrt(
        (vec2[0] - vec1[0]) ** 2 + (vec2[1] - vec1[1]) ** 2 + (vec2[2] - vec1[2]) ** 2
    )
