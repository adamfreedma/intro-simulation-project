from resetable_walker import ResetableWalker
import math


def test_init() -> None:
    walker = ResetableWalker("Walker1", True, 2.5)
    assert walker.get_name() == "Walker1"
    assert walker.is_3d() == True
    assert walker.get_mass() == 2.5


def test_generate_move_radius() -> None:
    walker = ResetableWalker("Walker1", True, 2.5)
    radius = walker._generate_move_radius()
    assert isinstance(radius, float)
    assert radius >= 0


def test_generate_move_angle() -> None:
    walker = ResetableWalker("Walker1", True, 2.5)
    walker2d = ResetableWalker("Walker1", False, 2.5)
    angle = walker._generate_move_angle()
    assert isinstance(angle, tuple)
    assert len(angle) == 2
    assert angle[0] >= 0 and angle[0] <= 2 * math.pi
    assert angle[1] >= 0 and angle[1] <= 2 * math.pi
    yaw, pitch = walker2d._generate_move_angle()
    assert pitch == 0
    assert yaw >= 0 and yaw <= 2 * math.pi
