import pytest
from teleporter import Teleporter


@pytest.fixture
def teleporter() -> Teleporter:
    location = (1.0, 2.0, 3.0)
    radius = 1.5
    target = (4.0, 5.0, 6.0)
    return Teleporter(location, radius, target)


def test_teleporter_init(teleporter: Teleporter) -> None:

    assert teleporter.get_location() == (1.0, 2.0, 3.0)
    assert teleporter.get_radius() == 1.5
    assert teleporter.get_target() == (4.0, 5.0, 6.0)


def test_teleporter_get_target(teleporter: Teleporter) -> None:
    assert teleporter.get_target() == (4.0, 5.0, 6.0)
