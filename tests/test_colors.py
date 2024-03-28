import pytest
from colors import WHITE, RED, GREEN

def test_white_color() -> None:
    assert WHITE == "#ffffff"

def test_red_color() -> None:
    assert RED == "#ff0000"

def test_green_color() -> None:
    assert GREEN == "#00ff00"

def test_invalid_color() -> None:
    with pytest.raises(NameError):
        assert BLUE == "#0000ff" # type: ignore[name-defined]
