import pytest
from random_walker import RandomWalker
import math


@pytest.fixture
def random_walker() -> RandomWalker:
    return RandomWalker("Test Walker", is_3d=False, mass=1)


def test_random_walker_init(random_walker: RandomWalker) -> None:
    assert random_walker.get_name() == "Test Walker"
    assert random_walker.is_3d() == False
    assert random_walker.get_mass() == 1


def test_generate_move_radius(random_walker: RandomWalker) -> None:
    move_radius = random_walker._generate_move_radius()
    assert isinstance(move_radius, float)
    assert move_radius >= 0


def test_generate_move_angle(random_walker: RandomWalker) -> None:
    walker2d = RandomWalker("Test Walker", is_3d=False, mass=1)
    angle = random_walker._generate_move_angle()
    assert isinstance(angle, tuple)
    assert len(angle) == 2
    assert angle[0] >= 0 and angle[0] <= 2 * math.pi
    assert angle[1] >= 0 and angle[1] <= 2 * math.pi
    assert angle[0] >= 0 and angle[0] < 360
    assert angle[1] >= -90 and angle[1] <= 90
    yaw, pitch = walker2d._generate_move_angle()
    assert pitch == 0
    assert yaw >= 0 and yaw <= 2 * math.pi
