import pytest
from grid import Grid
from obstacle import Obstacle
from straight_walker import StraightWalker
from move import Move
from teleporter import Teleporter
from speed_zone import SpeedZone
import math
from typing import List
from walker import Walker


@pytest.fixture
def grid() -> Grid:
    return Grid()


def test_clear_obstacles(grid: Grid) -> None:
    # Add some obstacles to the grid
    obstacle1 = Obstacle((1, 1, 1), 1)
    obstacle2 = Obstacle((2, 2, 2), 1)
    grid.set_obstacles([obstacle1, obstacle2])

    # Clear the obstacles
    grid.clear_obstacles()

    # Check that the obstacles list is empty
    assert len(grid.get_obstacles()) == 0


def test_find_closest(grid: Grid) -> None:
    # Create a list of obstacles
    obstacles = [Obstacle((1, 1, 1), 1), Obstacle((2, 2, 2), 1), Obstacle((3, 3, 3), 1)]

    # Set the starting location
    starting_location = (0, 0, 0)

    # Find the closest obstacle
    closest_obstacle = grid.find_closest(obstacles, starting_location)

    # Check that the closest obstacle is the expected one
    assert closest_obstacle == obstacles[0]


def test_get_gravity_effect(grid: Grid) -> None:
    # Create a walker and a list of walkers
    walker = StraightWalker("Josh", False)
    walker_list: List[Walker] = [
        StraightWalker("Josh", False),
        StraightWalker("Josh", False),
    ]

    # Get the gravity effect for the walker
    gravity_effect = grid.get_gravity_effect(walker, walker_list)
    # Check that the gravity effect is calculated correctly
    assert math.isclose(gravity_effect.angle_and_radius()[1], 0.0)


def test_move(grid: Grid) -> None:
    # Create a walker, a move, a list of walkers, and a list of obstacles
    walker = StraightWalker("Josh", False)
    move = Move(0, 1)

    # Move the walker
    grid.move(walker, move, [])
    grid.move(walker, move, [], [Teleporter((2, 0, 0), 0.5, (100, 0, 0))])
    grid.move(
        walker, move, [], [Obstacle((105, 0, 0), 1), SpeedZone((100, 0, 0), 1, 100)]
    )

    # Check that the walker's position is updated correctly
    assert walker.get_location() == (100, 0, 0)


def test_add_teleporters(grid: Grid) -> None:
    # Add teleporters from a valid file path
    assert grid.add_teleporters("config.json") == True
    assert grid.add_teleporters("bad config.json") == False

    # Add teleporters from an invalid file path
    assert grid.add_teleporters("a.json") == False


def test_add_obstacles(grid: Grid) -> None:
    # Add obstacles from a valid file path
    assert grid.add_obstacles("config.json") == True
    assert grid.add_obstacles("bad config.json") == False

    # Add obstacles from an invalid file path
    assert grid.add_obstacles("a.json") == False


def test_add_speed_zones(grid: Grid) -> None:
    # Add speed zones from a valid file path
    assert grid.add_speed_zones("config.json") == True
    assert grid.add_speed_zones("bad config.json") == False

    # Add speed zones from an invalid file path
    assert grid.add_speed_zones("a.json") == False


def test_set_obstacles(grid: Grid) -> None:
    # Create a list of obstacles
    obstacles = [Obstacle((1, 1, 1), 1), Obstacle((2, 2, 2), 1), Obstacle((3, 3, 3), 1)]

    # Set the obstacles in the grid
    grid.set_obstacles(obstacles)

    # Check that the obstacles are set correctly
    assert grid.get_obstacles() == obstacles


def test_get_obstacles(grid: Grid) -> None:
    # Get the obstacles from an empty grid
    assert grid.get_obstacles() == []

    # Add some obstacles to the grid
    obstacle1 = Obstacle((1, 1, 1), 1)
    obstacle2 = Obstacle((2, 2, 2), 1)
    grid.set_obstacles([obstacle1, obstacle2])

    # Get the obstacles from the grid
    obstacles = grid.get_obstacles()

    # Check that the obstacles list is returned correctly
    assert obstacles == [obstacle1, obstacle2]
