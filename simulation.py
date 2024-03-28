from grid import Grid
from walker import Walker
import numpy as np
import json
import graph
from screen import Screen
import time
from threading import Event
from customtkinter import DoubleVar # type: ignore[import]
from typing import List, Dict


class Simulation:

    __LEAVE_DISTANCE = 10
    __EPSILON = 0.0001
    __LOGS_FOLDER = "logs/"

    def __init__(
        self,
        grid: Grid,
        screen: Screen,
        simulation_count: int=10,
        max_steps: int=10,
    ) -> None:
        self.__grid = grid
        self.__screen = screen
        self.__simulation_count = simulation_count
        self.__max_steps = max_steps
        self.__wait = 0.001

    def config(self, path: str) -> bool:
        self.__grid.clear_obstacles()
        success = self.__grid.add_teleporters(path) and self.__grid.add_obstacles(path) and self.__grid.add_speed_zones(path)
        self.__screen.set_obstacles(self.__grid.get_obstacles())
    
        return success
    
    def set_simulation_count(self, simulation_count: int) -> None:
        self.__simulation_count = simulation_count
    
    def get_simulation_count(self) -> int:
        return self.__simulation_count
    
    def set_max_steps(self, max_steps: int) -> None:
        self.__max_steps = max_steps
    
    def get_max_steps(self) -> int:
        return self.__max_steps

    def _save_log_data(self, path: str, distance_list: List[float],
                       x_distance_list: List[float], y_distance_list: List[float],
                       z_distance_list: List[float], average_time_to_leave: float,
                       y_cross_count_list: List[float]) -> None:
        data = {
            "distance": distance_list,
            "xdistance": x_distance_list,
            "ydistance": y_distance_list,
            "zdistance": z_distance_list,
            "time_to_leave": average_time_to_leave,
            "y_cross_count_list": y_cross_count_list,
        }

        with open(path, "w") as f:
            json.dump(data, f)

    def wait_for_all(self, simulation: int, run_event_dict: Dict[Walker, Event], walker: Walker) -> None:
            # syncing the threads, on even runs setting the events, on odd runs unsetting the events
            if simulation % 2 == 0:
                set_dict = {walker : run_event_dict[walker].is_set() for walker in run_event_dict.keys()}
                run_event_dict[walker].set()
                while not all(set_dict.values()):
                    for walker, event in run_event_dict.items():
                        if event.is_set():
                            set_dict[walker] = True
                    time.sleep(0.01)
            else:
                set_dict = {walker : run_event_dict[walker].is_set() for walker in run_event_dict.keys()}
                run_event_dict[walker].clear()
                while any(set_dict.values()):
                    for walker, event in run_event_dict.items():
                        if not event.is_set():
                            set_dict[walker] = False
                    time.sleep(0.01)

    def simulate(self, walker: Walker, stop_event: Event,
                 run_event_dict: Dict[Walker, Event], progress_var: DoubleVar,
                 walker_list: List[Walker], visual:bool=False,
                 graph_output_path:str="") -> None:
        distance_list = [0.0] * self.__max_steps
        x_distance_list = [0.0] * self.__max_steps
        y_distance_list = [0.0] * self.__max_steps
        z_distance_list = [0.0] * self.__max_steps
        average_time_to_leave = 0.0
        y_cross_count_list = [0.0] * self.__max_steps
        
        self.__screen.add_walker(walker)

        for simulation in range(self.__simulation_count):
            if simulation >= self.__simulation_count:
                break
            
            self.__screen.reset_trail(walker)
            walker.reset()
            progress_var.set(float(simulation) / self.__simulation_count)

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
                distance = float(np.linalg.norm(location)) # type: ignore[no-untyped-call]
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

                distance_list[step] += distance / float(self.__simulation_count)
                x_distance_list[step] += abs(location[0]) / float(self.__simulation_count)
                y_distance_list[step] += abs(location[1]) / float(self.__simulation_count)
                z_distance_list[step] += abs(location[2]) / float(self.__simulation_count)

                self.__screen.add_to_trail(walker, walker.get_location())
                

            average_time_to_leave += time_to_leave / float(self.__max_steps)
            
            if stop_event.is_set():
                break
            
            self.wait_for_all(simulation, run_event_dict, walker)

        self.__screen.remove_walker(walker)

        log_path = f"{self.__LOGS_FOLDER}{walker.get_name()}.json"
        self._save_log_data(log_path, distance_list, x_distance_list,
                            y_distance_list, z_distance_list,
                            average_time_to_leave, y_cross_count_list)
        
        if graph_output_path:
            self.generate_graphs(log_path, graph_output_path, walker.is_3d())

    def run_visual(self, event: Event) -> None:
        self.__screen.run(event)
        
    def update_speed(self, value: float) -> None:
        self.__wait = (1.001 - value) / 10
        
    def get_wait(self) -> float:
        return self.__wait
        
    def stop(self) -> None:
        self.__screen.stop()

    def close(self) -> None:
        self.__screen.close()

    def get_stop(self) -> bool:
        return self.__screen.get_stop()

    def generate_graphs(self, log_path: str, output_path: str, is_3d: bool) -> None:
        graph.distance_graph(log_path, output_path)
        graph.distance_graph(log_path, output_path, "x")
        graph.distance_graph(log_path, output_path, "y")
        graph.cross_amount_graph(log_path, output_path)
        if is_3d:
            graph.distance_graph(log_path, output_path, "z")
