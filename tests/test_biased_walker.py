import pytest
from biased_walker import BiasedWalker
import math


@pytest.fixture
def biased_walker() -> BiasedWalker:
    return BiasedWalker(
        "Test Walker", is_3d=True, mass=1.0, bias="Origin", bias_scale=2
    )


def test_biased_walker_init(biased_walker: BiasedWalker) -> None:
    assert biased_walker.get_name() == "Test Walker"
    assert biased_walker.is_3d() == True
    assert biased_walker.get_mass() == 1.0
    assert biased_walker.bias == "Origin"
    assert biased_walker.bias_scale == 2


def test_generate_move_angle_2d() -> None:
    biased_walker = BiasedWalker(
        "Test Walker", is_3d=False, mass=1.0, bias="Left", bias_scale=2
    )
    move_angle = biased_walker._generate_move_angle()

    assert isinstance(move_angle, tuple)


def test_biased_walker_not_in_dict() -> None:
    walker = BiasedWalker(
        "Test Walker", is_3d=True, mass=1.0, bias="invalid", bias_scale=2
    )
    assert walker.bias in BiasedWalker.BIAS_DICT.keys()


def test_biased_walker_generate_move_radius(biased_walker: BiasedWalker) -> None:
    move_radius = biased_walker._generate_move_radius()
    assert isinstance(move_radius, float)
    assert move_radius == 1.0


def test_biased_walker_generate_move_angle(biased_walker: BiasedWalker) -> None:
    walker2d = BiasedWalker("Walker1", False, 2.5, "Origin", 2)
    angle = biased_walker._generate_move_angle()
    assert isinstance(angle, tuple)
    assert len(angle) == 2
    assert angle[0] >= 0 and angle[0] <= 2 * math.pi
    assert angle[1] >= 0 and angle[1] <= 2 * math.pi
    yaw, pitch = walker2d._generate_move_angle()
    assert pitch == 0
    assert yaw >= 0 and yaw <= 2 * math.pi
