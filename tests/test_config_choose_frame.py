import pytest
from config_choose_frame import ConfigChooseFrame
from main_frame import MainFrame
from main import MainApp
from simulation import Simulation
from grid import Grid
from screen import Screen
import customtkinter as ctk # type: ignore[import]

@pytest.fixture
def config_choose_frame() -> ConfigChooseFrame:
    # Create an instance of ConfigChooseFrame for testing
    return ConfigChooseFrame(MainFrame(ctk.CTkTabview(ctk.CTk()).add("A"), MainApp(), Simulation(Grid(), Screen(800, 600))))

def test_file_dialog(config_choose_frame: ConfigChooseFrame) -> None:
    # Test the file_dialog method
    try:
        config_choose_frame.file_dialog(False)
    except Exception as e:
        assert False

    assert True

def test_init(config_choose_frame: ConfigChooseFrame) -> None:
    # Add your test code here
    assert isinstance(config_choose_frame, ConfigChooseFrame)

