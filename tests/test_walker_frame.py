import pytest
from grid import Grid
from main import MainApp
from main_frame import MainFrame
from screen import Screen
from simulation import Simulation
from straight_walker import StraightWalker
from walker_frame import WalkerFrame, Walker
from walker_config_frame import WalkerConfigFrame
import customtkinter as ctk  # type: ignore[import]


@pytest.fixture
def walker_frame():
    return WalkerFrame(
        WalkerConfigFrame(
            MainFrame(
                ctk.CTkTabview(ctk.CTk()).add("A"),
                MainApp(),
                Simulation(Grid(), Screen(800, 600)),
            )
        )
    )


def test_get_walker(walker_frame):
    walker_frame.master.create_walker()
    walker = walker_frame.get_walker("0")
    assert isinstance(walker, StraightWalker)


def test_pack_walker_specific_widgets(walker_frame):
    error = False
    try:
        walker_frame.pack_walker_specific_widgets("Biased")
        walker_frame.pack_walker_specific_widgets("Accelerating")
        walker_frame.pack_walker_specific_widgets("invalid")
    except Exception:
        error = True

    assert error == False


def test_delete(walker_frame):
    walker_frame.master.create_walker()
    master = walker_frame.master
    walker_frame.delete()

    assert walker_frame not in master.walker_frame_list


def test_walker_frame_init(walker_frame):
    assert isinstance(walker_frame.get_walker("2"), StraightWalker)
