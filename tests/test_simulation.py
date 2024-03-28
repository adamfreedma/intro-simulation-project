import time
import pytest
from simulation import Simulation
from grid import Grid
from screen import Screen
from straight_walker import StraightWalker
from threading import Event
from customtkinter import DoubleVar # type: ignore[import]
import os
import threading
from typing import List, Dict

from walker import Walker

@pytest.fixture
def simulation() -> Simulation:
    grid = Grid()
    screen = Screen(800, 600)
    return Simulation(grid, screen)

def test_set_simulation_count(simulation: Simulation) -> None:
    simulation.set_simulation_count(100)
    assert simulation.get_simulation_count() == 100

def test_set_max_steps(simulation: Simulation) -> None:
    simulation.set_max_steps(5000)
    assert simulation.get_max_steps() == 5000

def test_config(simulation: Simulation) -> None:
    assert simulation.config("config.json") == True

def test_save_log_data(simulation: Simulation) -> None:
    distance_list = [1.0, 2.0, 3.0]
    x_distance_list = [0.5, 1.0, 1.5]
    y_distance_list = [0.2, 0.4, 0.6]
    z_distance_list = [0.1, 0.2, 0.3]
    average_time_to_leave = 10.0
    y_cross_count_list = [5.0, 10.0, 15.0]
    simulation._save_log_data("log.txt", distance_list, x_distance_list, y_distance_list, z_distance_list, average_time_to_leave, y_cross_count_list)
    
    assert os.path.exists("log.txt")


def test_simulate(simulation: Simulation) -> None:
    walker = StraightWalker("Josh", False)
    stop_event = Event()
    run_event_dict: Dict[Walker, Event] = {walker: Event()}
    progress_var = DoubleVar()
    walker_list: List[Walker] = [walker]
    simulation.simulate(walker, stop_event, run_event_dict, progress_var, walker_list, True, "test")
    simulation.close()
    
    assert os.path.exists("test-xdistance.png")
    assert os.path.exists("test-ydistance.png")
    
    os.remove("test-xdistance.png")
    os.remove("test-ydistance.png")

def test_run_visual(simulation: Simulation) -> None:
    event = threading.Event()
    run_thread = threading.Thread(target=simulation.run_visual, args=(event,))
    run_thread.start()
    time.sleep(0.1)
    simulation.stop()
    run_thread.join()
    assert simulation.get_stop()
    simulation.close()
    

def test_update_speed(simulation: Simulation) -> None:
    value = 1.5
    simulation.update_speed(value)

    assert simulation.get_wait() == (1.001 - value) / 10

def test_stop(simulation: Simulation) -> None:
    simulation.stop()
    assert simulation.get_stop() == True

def test_generate_graphs(simulation: Simulation) -> None:
    simulation.generate_graphs("log.txt", "test", True)
    
    assert os.path.exists("test-xdistance.png")
    assert os.path.exists("test-ydistance.png")
    assert os.path.exists("test-zdistance.png")
    assert os.path.exists("test-distance.png")
    assert os.path.exists("test-cross-count.png")
        
    os.remove("test-xdistance.png")
    os.remove("test-ydistance.png")
    os.remove("test-zdistance.png")
    os.remove("test-cross-count.png")
    os.remove("test-distance.png")
    os.remove("log.txt")


