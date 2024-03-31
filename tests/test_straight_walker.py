import pytest
from straight_walker import StraightWalker
import math


@pytest.fixture
def straight_walker() -> StraightWalker:
    return StraightWalker("Test Walker", is_3d=True, mass=1)


def test_init(straight_walker: StraightWalker) -> None:
    assert straight_walker.get_name() == "Test Walker"
    assert straight_walker.is_3d() == True
    assert straight_walker.get_mass() == 1


def test_generate_move_radius(straight_walker: StraightWalker) -> None:
    radius = straight_walker._generate_move_radius()
    assert isinstance(radius, float)
    assert radius >= 0


def test_generate_move_angle(straight_walker: StraightWalker) -> None:
    angle = straight_walker._generate_move_angle()
    assert isinstance(angle, tuple)
    assert len(angle) == 2
    assert angle[0] >= 0 and angle[0] <= 2 * math.pi
    assert angle[1] >= 0 and angle[1] <= 2 * math.pi

    walker2d = StraightWalker("Test Walker", is_3d=False, mass=1)
    yaw, pitch = walker2d._generate_move_angle()
    assert pitch == 0.0
    assert yaw >= 0 and yaw <= 2 * math.pi
