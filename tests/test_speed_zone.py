from speed_zone import SpeedZone
from obstacle import Obstacle


def test_speed_zone_init() -> None:
    location = (1.0, 2.0, 3.0)
    radius = 5.0
    speed_factor = 2.0
    speed_zone = SpeedZone(location, radius, speed_factor)
    assert isinstance(speed_zone, Obstacle)
    assert speed_zone.get_location() == location
    assert speed_zone.get_radius() == radius
    assert speed_zone.get_speed_factor() == speed_factor


def test_speed_zone_get_speed_factor() -> None:
    location = (1.0, 2.0, 3.0)
    radius = 5.0
    speed_factor = 0.5
    speed_zone = SpeedZone(location, radius, speed_factor)
    assert speed_zone.get_speed_factor() == speed_factor


def test_speed_zone_get_color() -> None:
    location = (1.0, 2.0, 3.0)
    radius = 5.0
    speed_factor = 2.0
    speed_zone = SpeedZone(location, radius, speed_factor)
    assert isinstance(speed_zone.get_color(), tuple)
    assert len(speed_zone.get_color()) == 3
    assert speed_zone.get_color()[0] == 1

    location = (1.0, 2.0, 3.0)
    radius = 5.0
    speed_factor = 0.5
    speed_zone = SpeedZone(location, radius, speed_factor)
    assert isinstance(speed_zone.get_color(), tuple)
    assert len(speed_zone.get_color()) == 3
    assert speed_zone.get_color()[1] == 1
