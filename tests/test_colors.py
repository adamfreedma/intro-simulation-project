import pytest
from colors import Colors


def test_white_color() -> None:
    assert Colors.WHITE == "#ffffff"


def test_red_color() -> None:
    assert Colors.RED == "#ff0000"


def test_green_color() -> None:
    assert Colors.GREEN == "#00ff00"


def test_invalid_color() -> None:
    with pytest.raises(AttributeError):
        assert Colors.BLUE == "#0000ff"  # type: ignore[attr-defined]
