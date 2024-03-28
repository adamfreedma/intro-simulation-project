import pytest
from start_frame import StartFrame
from main_frame import MainFrame
import customtkinter as ctk # type: ignore[import]
from simulation import Simulation
from grid import Grid
from main import MainApp
from screen import Screen

@pytest.fixture
def start_frame() -> StartFrame:
    # Create a StartFrame instance for testing
    return StartFrame(MainFrame(ctk.CTkTabview(ctk.CTk()).add("A"), MainApp(), Simulation(Grid(), Screen(800, 600))))

def test_start_frame_init(start_frame: StartFrame) -> None:
    # Test the __init__ method
    assert isinstance(start_frame, StartFrame)


def test_start_frame_update_speed(start_frame: StartFrame) -> None:
    start_frame.update_speed(1)
    
    assert start_frame.get_speed() == 1

def test_start_frame_update_simulation_count(start_frame: StartFrame) -> None:
    start_frame.update_simulation_count(100)
    
    assert start_frame.get_simulation_count() == 100

def test_start_frame_update_max_steps(start_frame):
    start_frame.update_max_steps(100)
    
    assert start_frame.get_max_steps() == 100

def test_start_frame_stop(start_frame: StartFrame) -> None:
    start_frame.stop()
    
    assert start_frame.progress_bar.winfo_ismapped() == False
