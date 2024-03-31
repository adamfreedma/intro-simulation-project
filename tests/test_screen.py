from re import T
import pytest
from resetable_walker import ResetableWalker
from screen import Screen
from stock_walker import StockWalker
from straight_walker import StraightWalker
from obstacle import Obstacle
from teleporter import Teleporter
from speed_zone import SpeedZone
import threading
import time


@pytest.fixture
def screen() -> Screen:
    return Screen(800, 600)


def test_initialize(screen: Screen) -> None:
    screen.initialize()
    assert screen.get_stop() == False

    screen.close()


def test_add_and_remove_walker(screen: Screen) -> None:
    walker = StockWalker("Josh", False)
    screen.add_walker(walker)
    assert walker in screen.get_walkers()
    screen.remove_walker(walker)
    assert walker not in screen.get_walkers()


def test_reset_trail(screen: Screen) -> None:
    walker = ResetableWalker("Josh", False)
    screen.add_walker(walker)
    screen.reset_trail(walker)
    assert screen.get_trails()[walker] == []


def test_add_to_trail(screen: Screen) -> None:
    walker = StraightWalker("Josh", False)
    screen.add_walker(walker)
    position = (1, 2, 3)
    screen.add_to_trail(walker, position)
    assert screen.get_trails()[walker] == [position]


def test_set_obstacles(screen: Screen) -> None:
    obstacles = [Obstacle((1, 1, 1), 1), Obstacle((2, 2, 2), 1)]
    screen.set_obstacles(obstacles)
    assert screen.get_obstacles() == obstacles


def test_draw_line(screen: Screen) -> None:
    screen.initialize()

    screen.draw_line((-screen.INF, 0, 0), (screen.INF, 0, 0), (1, 0, 0))

    assert True
    screen.close()


def test_render_sphere(screen: Screen) -> None:
    screen.initialize()
    location = (0, 0, 0)
    radius = 1.0
    color = (1, 0, 0)

    screen.render_sphere(location, radius, color)

    assert True
    screen.close()


def test_render_all(screen: Screen) -> None:
    walker = StraightWalker("Josh", False)
    screen.add_walker(walker)
    screen.add_to_trail(walker, (1, 1, 1))
    screen.set_obstacles(
        [
            Obstacle((1, 1, 1), 1),
            Teleporter((1, 1, 1), 1, (2, 2, 2)),
            SpeedZone((1, 1, 1), 1, 1),
        ]
    )
    screen.initialize()

    screen.render_all()

    assert True
    screen.close()


def test_move(screen: Screen) -> None:
    screen.initialize()
    movement = (1, 0, 0)
    screen.move(movement)

    assert True
    screen.close()
