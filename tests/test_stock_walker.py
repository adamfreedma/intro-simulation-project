import pytest
from stock_walker import StockWalker
import math


@pytest.fixture
def stock_walker() -> StockWalker:
    return StockWalker("Test Walker", mass=1)


def test_stock_walker_init(stock_walker: StockWalker) -> None:
    assert stock_walker.get_name() == "Test Walker"
    assert stock_walker.is_3d() == False
    assert stock_walker.get_mass() == 1


def test_generate_move_radius(stock_walker: StockWalker) -> None:
    move_radius = stock_walker._generate_move_radius()
    assert isinstance(move_radius, float)
    assert move_radius >= 0


def test_generate_move_angle(stock_walker: StockWalker) -> None:
    angle = stock_walker._generate_move_angle()
    assert isinstance(angle, tuple)
    assert len(angle) == 2
    assert angle[0] == math.pi / 2 or angle[0] == -math.pi / 2
    
def test_choose_random_stock(stock_walker: StockWalker) -> None:
    assert len(stock_walker._choose_random_stock()) >= 1000
    
def test_reset(stock_walker: StockWalker) -> None:
    stock_walker.reset()
    assert stock_walker.get_step() == 1
