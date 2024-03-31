import os
from grid import Grid
from walker import Walker
import numpy as np
import json
import graph
from screen import Screen
import time
from threading import Event
from customtkinter import DoubleVar  # type: ignore[import]
from typing import List, Dict


class Simulation:

    __LEAVE_DISTANCE = 10
    __EPSILON = 0.0001
    __LOGS_FOLDER = "logs/"

    def __init__(
        self,
        grid: Grid,
        screen: Screen,
        simulation_count: int = 10,
        max_steps: int = 10,
    ) -> None:
        """Initializes a Simulation object.

        Args:
            grid (Grid): A Grid object.
            screen (Screen): _description_
            simulation_count (int, optional): _description_. Defaults to 10.
            max_steps (int, optional): _description_. Defaults to 10.
        """
        self.__grid = grid
        self.__screen = screen
        self.__simulation_count = simulation_count
        self.__max_steps = max_steps
        self.__wait = 0.001

    def config(self, path: str) -> bool:
        """Configures the simulation from a config file.

        Args:
            path (str): The path to the config file.

        Returns:
            bool: Was the config succesfull.
        """
        self.__grid.clear_obstacles()
        success = (
            self.__grid.add_teleporters(path)
            and self.__grid.add_obstacles(path)
            and self.__grid.add_speed_zones(path)
        )
        self.__screen.set_obstacles(self.__grid.get_obstacles())

        return success

    def set_simulation_count(self, simulation_count: int) -> None:
        """Sets the simulation count.

        Args:
            simulation_count (int): The simulation count.
        """
        self.__simulation_count = simulation_count

    def get_simulation_count(self) -> int:
        """Get the simulation count.

        Returns:
            int: The simulation count.
        """
        return self.__simulation_count

    def set_max_steps(self, max_steps: int) -> None:
        """Set the max steps.

        Args:
            max_steps (int): The max steps.
        """
        self.__max_steps = max_steps

    def get_max_steps(self) -> int:
        """Gets the max steps.

        Returns:
            int: The max steps.
        """
        return self.__max_steps

    def _save_log_data(
        self,
        path: str,
        distance_list: List[float],
        x_distance_list: List[float],
        y_distance_list: List[float],
        z_distance_list: List[float],
        center_mass_distance_list: List[float],
        average_time_to_leave_list: List[float],
        y_cross_count_list: List[float],
    ) -> None:
        """Saves the data to

        Args:
            path (str): tTe path to save the log file in.
            distance_list (List[float]): The distance data list.
            x_distance_list (List[float]): The distance in the x axis data list.
            y_distance_list (List[float]): The distance in the y axis data list.
            z_distance_list (List[float]): The distance in the z axis data list.
            center_mass_distance_list (List[float]): The distance from the center mass data list.
            average_time_to_leave (float): The average time to leave.
            y_cross_count_list (List[float]): The cross count list data lis.
        """
        data = {
            "distance": distance_list,
            "xdistance": x_distance_list,
            "ydistance": y_distance_list,
            "zdistance": z_distance_list,
            "cmdistance": center_mass_distance_list,
            "time_to_leave": average_time_to_leave_list,
            "y_cross_count_list": y_cross_count_list,
        }
        # making the logs folder if it dose not exist
        if not os.path.isdir(self.__LOGS_FOLDER):
            os.mkdir(self.__LOGS_FOLDER)

        with open(path, "w") as f:
            json.dump(data, f)

    def wait_for_all(
        self, simulation: int, run_event_dict: Dict[Walker, Event], walker: Walker
    ) -> None:
        """Waits for all walkers to finish the current simulation.

        Args:
            simulation (int): The current simulation index.
            run_event_dict (Dict[Walker, Event]): The dict of the threads running.
            walker (Walker): Current walker.
        """
        # syncing the threads, on even runs setting the events, on odd runs unsetting the events
        if simulation % 2 == 0:
            set_dict = {
                walker: run_event_dict[walker].is_set()
                for walker in run_event_dict.keys()
            }
            # setting the event
            run_event_dict[walker].set()
            # waiting for all other threads
            while not all(set_dict.values()):
                for walker, event in run_event_dict.items():
                    if event.is_set():
                        set_dict[walker] = True
                time.sleep(0.01)
        else:
            set_dict = {
                walker: run_event_dict[walker].is_set()
                for walker in run_event_dict.keys()
            }
            # setting the event
            run_event_dict[walker].clear()
            # waiting for all other threads
            while any(set_dict.values()):
                for walker, event in run_event_dict.items():
                    if not event.is_set():
                        set_dict[walker] = False
                time.sleep(0.01)

    def simulate(
        self,
        walker: Walker,
        stop_event: Event,
        run_event_dict: Dict[Walker, Event],
        progress_var: DoubleVar,
        walker_list: List[Walker],
        visual: bool = False,
        graph_output_path: str = "",
    ) -> None:
        """Simulation main loop

        Args:
            walker (Walker): The walker to simulate.
            stop_event (Event): The stop event.
            run_event_dict (Dict[Walker, Event]): The dict of the threads running.
            progress_var (DoubleVar): The progress bar variable.
            walker_list (List[Walker]): The list of all walkers.
            visual (bool, optional): Add to the screen. Defaults to False.
            graph_output_path (str, optional): The output folder to save graphs. Defaults to "".
        """
        # initializes the data lists
        distance_list = [0.0] * self.__max_steps
        x_distance_list = [0.0] * self.__max_steps
        y_distance_list = [0.0] * self.__max_steps
        z_distance_list = [0.0] * self.__max_steps
        center_mass_distance_list = [0.0] * self.__max_steps
        average_time_to_leave_list = [0.0] * self.__simulation_count
        y_cross_count_list = [0.0] * self.__max_steps
        # adds the walker to the screen
        self.__screen.add_walker(walker)

        for simulation in range(self.__simulation_count):
            if simulation >= self.__simulation_count:
                break
            # reseting the trail
            self.__screen.reset_trail(walker)
            walker.reset()
            progress_var.set(float(simulation) / self.__simulation_count)
            # reseting the variables
            cross_count = 0
            sign = 0
            time_to_leave = -1

            for step in range(self.__max_steps):
                if stop_event.is_set() or step >= self.__max_steps:
                    break
                if visual:
                    time.sleep(self.__wait)

                self.__grid.move(walker, walker.get_move(), walker_list)

                location = walker.get_location()
                distance = float(np.linalg.norm(location))  # type: ignore[no-untyped-call]
                center_mass_distance = float(np.linalg.norm(np.subtract(
                    location, np.average([other_walker.get_location()
                                          for other_walker in walker_list], axis=0))))  # type: ignore[no-untyped-call]
                if walker.is_3d():
                    distance = float(np.linalg.norm(location[:2]))  # type: ignore[no-untyped-call]
                # tracking  y axis crosses
                if location[1] - self.__EPSILON > 0:
                    if sign == -1:
                        cross_count += 1
                    sign = 1
                if location[1] + self.__EPSILON < 0:
                    if sign == 1:
                        cross_count += 1
                    sign = -1
                y_cross_count_list[step] += cross_count / float(self.__simulation_count)
                # tracking time to leave
                if time_to_leave == -1 and distance > self.__LEAVE_DISTANCE:
                    time_to_leave = step + 1
                # tracking distances
                distance_list[step] += distance / float(self.__simulation_count)
                x_distance_list[step] += abs(location[0]) / float(
                    self.__simulation_count
                )
                y_distance_list[step] += abs(location[1]) / float(
                    self.__simulation_count
                )
                z_distance_list[step] += abs(location[2]) / float(
                    self.__simulation_count
                )
                center_mass_distance_list[step] += abs(center_mass_distance) / float(
                    self.__simulation_count
                )

                self.__screen.add_to_trail(walker, walker.get_location())

            average_time_to_leave_list[simulation] = time_to_leave

            if stop_event.is_set():
                break

            # waiting for all the other walkers
            self.wait_for_all(simulation, run_event_dict, walker)

        self.__screen.remove_walker(walker)

        log_path = f"{self.__LOGS_FOLDER}{walker.get_name()}.json"
        # logging the data
        self._save_log_data(
            log_path,
            distance_list,
            x_distance_list,
            y_distance_list,
            z_distance_list,
            center_mass_distance_list,
            average_time_to_leave_list,
            y_cross_count_list,
        )

        # generating the graphs
        if graph_output_path:
            self.generate_graphs(log_path, graph_output_path, walker.is_3d())

    def run_visual(self, event: Event) -> None:
        """Run the screen.

        Args:
            event (Event): the stop event.
        """
        self.__screen.run(event)

    def update_speed(self, value: float) -> None:
        """Update the speed.

        Args:
            value (float): the speed to set.
        """
        self.__wait = (1.001 - value) / 10

    def get_wait(self) -> float:
        """Get the wait per frame.

        Returns:
            float: The wait time.
        """
        return self.__wait

    def stop(self) -> None:
        """Stops the scren.
        """
        self.__screen.stop()

    def close(self) -> None:
        """Closes the screen.
        """
        self.__screen.close()

    def get_stop(self) -> bool:
        """Return if the screen is stopped.

        Returns:
            bool: Is the screen stopped.
        """
        return self.__screen.get_stop()

    def generate_graphs(self, log_path: str, output_path: str, is_3d: bool) -> None:
        """Generates and saves the graphs

        Args:
            log_path (str): The data log path.
            output_path (str): The graph picture folder.
            is_3d (bool): is the data in 3d (should we generate a z distance graph).
        """
        graph.distance_graph(log_path, output_path)
        graph.distance_graph(log_path, output_path, "x")
        graph.distance_graph(log_path, output_path, "y")
        graph.distance_graph(log_path, output_path, "cm")
        graph.cross_count_graph(log_path, output_path)
        graph.time_to_leave_graph(log_path, output_path)
        if is_3d:
            graph.distance_graph(log_path, output_path, "z")
