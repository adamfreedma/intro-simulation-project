from accelerating_walker import AcceleratingWalker
import math

def test_accelerating_walker_init() -> None:
    walker = AcceleratingWalker("John", False, 2.5, "Quadratic")
    walker_wrong = AcceleratingWalker("John", False, 2.5, "wrong")
    assert walker.get_name() == "John"
    assert walker.is_3d() == False
    assert walker.get_mass() == 2.5
    assert walker_wrong.get_acceleration_type() == "Linear"

def test_accelerating_walker_generate_move_radius() -> None:
    walker = AcceleratingWalker("John", False)
    radius = walker._generate_move_radius()
    assert isinstance(radius, float)
    assert radius >= 0

def test_accelerating_walker_generate_move_angle() -> None:
    walker = AcceleratingWalker("John", False)
    walker3d = AcceleratingWalker("John", True)
    angle = walker._generate_move_angle()
    assert isinstance(angle, tuple)
    assert len(angle) == 2
    assert angle[0] >= 0 and angle[0] <= 2 * math.pi
    assert angle[1] >= 0 and angle[1] <= 2 * math.pi
    yaw, pitch = walker3d._generate_move_angle()
    assert isinstance(yaw, float)
    assert isinstance(pitch, float)

def test_accelerating_walker_reset() -> None:
    walker = AcceleratingWalker("John", False)
    walker.move(walker.get_move())
    walker.move(walker.get_move())
    walker.move(walker.get_move())
    first_move_size = walker.get_move().angle_and_radius()[1]
    walker.reset()
    assert walker.get_move().angle_and_radius()[1] < first_move_size
