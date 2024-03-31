import pytest
import customtkinter as ctk  # type: ignore[import]
from main_frame import MainFrame
from main import MainApp
from simulation import Simulation
from grid import Grid
from screen import Screen
import os
import threading


@pytest.fixture
def main_frame() -> MainFrame:
    # Create an instance of MainFrame for testing
    return MainFrame(
        ctk.CTkTabview(ctk.CTk()).add("A"),
        MainApp(),
        Simulation(Grid(), Screen(800, 600)),
    )


def test_start_simulation(main_frame: MainFrame) -> None:
    # Test start_simulation method
    visual = False
    progress_var = ctk.DoubleVar()
    simulation_count = 10
    max_steps = 100
    graph_output_folder = "out"

    main_frame.start_simulation(
        visual, progress_var, simulation_count, max_steps, graph_output_folder
    )
    assert os.path.isdir(main_frame.get_folder_prefix() + graph_output_folder)


def example_function() -> None:
    pass


def test_wait_to_stop(main_frame: MainFrame) -> None:
    thread = threading.Thread(target=example_function)
    thread.start()
    # Test wait_to_stop method
    walker_thread_list = [thread]

    main_frame.wait_to_stop(walker_thread_list)

    assert main_frame.simulation.get_stop()


def test_update_speed(main_frame: MainFrame) -> None:
    # Test update_speed method
    value = 1.0

    main_frame.update_speed(value)

    assert main_frame.simulation.get_wait() == (1.001 - value) / 10


def test_update_simulation_count(main_frame: MainFrame) -> None:
    # Test update_simulation_count method
    value = 10

    main_frame.update_simulation_count(value)
    assert main_frame.simulation.get_simulation_count() == value


def test_update_max_steps(main_frame: MainFrame) -> None:
    # Test update_max_steps method
    value = 100

    main_frame.update_max_steps(value)

    assert main_frame.simulation.get_max_steps() == value


def test_parse_config(main_frame: MainFrame) -> None:
    # Test parse_config method

    result = main_frame.parse_config("config.json")

    assert result == True
