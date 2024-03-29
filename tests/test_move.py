from move import Move
import math


def test_init() -> None:
    move = Move(0.5, 1.0, 0.2)
    assert move.angle_and_radius()[0] == 0.5
    assert move.angle_and_radius()[1] == 1.0
    assert move.angle_and_radius()[2] == 0.2


def test_angle_and_radius() -> None:
    move = Move(0.5, 1.0, 0.2)
    angle, radius, pitch = move.angle_and_radius()
    assert angle == 0.5
    assert radius == 1.0


def test_scale_radius() -> None:
    move = Move(0.5, 1.0, 0.2)
    move.scale_radius(2.0)
    assert move.angle_and_radius()[1] == 2.0


def test_add() -> None:
    move1 = Move(0, 1.0, 0.2)
    move2 = Move(0, 1.0, 0.2)
    result = move1 + move2

    assert math.isclose(result.angle_and_radius()[0], 0)
    assert math.isclose(result.angle_and_radius()[1], 2.0)
    assert math.isclose(result.angle_and_radius()[2], 0.2)


def test_str() -> None:
    move = Move(0.5, 1.0, 0.2)
    assert str(move) == "yaw: 0.5, radius: 1.0, pitch: 0.2"
