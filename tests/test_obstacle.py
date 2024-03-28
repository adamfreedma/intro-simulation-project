import pytest
from obstacle import Obstacle


def test_obstacle_initialization() -> None:
    location = (1, 2, 3)
    radius = 5.0
    obstacle = Obstacle(location, radius)
    assert obstacle.get_location() == location
    assert obstacle.get_radius() == radius


def test_obstacle_collision_detection() -> None:
    obstacle = Obstacle((0, 0, 0), 5.0)
    
    # Test when there is no collision
    assert not obstacle.detect_colision((10, 10, 10), (20, 20, 20))
    assert not obstacle.detect_colision((10, 10, 10), (10, 20, 10))
    
    # Test when there is a collision
    assert obstacle.detect_colision((0, 0, 0), (3, 3, 3))


def test_obstacle_get_location() -> None:
    location = (1, 2, 3)
    obstacle = Obstacle(location, 5.0)
    assert obstacle.get_location() == location


def test_obstacle_get_radius() -> None:
    radius = 5.0
    obstacle = Obstacle((1, 2, 3), radius)
    assert obstacle.get_radius() == radius
