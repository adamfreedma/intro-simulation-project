from grid import Grid
from walker import Walker
import numpy as np
import json
import graph
from screen import Screen
import time
from threading import Event
from customtkinter import DoubleVar
from typing import List


class Simulation:

    __LEAVE_DISTANCE = 10
    __EPSILON = 0.0001
    __LOGS_FOLDER = "logs/"

    def __init__(
        self,
        grid: Grid,
        screen: Screen,
        simulation_count=50,
        max_steps=5000,
    ) -> None:
        self.__grid = grid
        self.__screen = screen
        self.__simulation_count = simulation_count
        self.__max_steps = max_steps

    def config(self, path: str):
        return self.config_obstacles(path) and self.config_teleporters(path)
    
    def config_teleporters(self, path: str):
        success = self.__grid._config_teleporters(path)
        self.__screen.set_teleporters(self.__grid.get_teleporters())
        return success

    def set_simulation_count(self, simulation_count: int):
        self.__simulation_count = simulation_count
        
    def set_max_steps(self, max_steps: int):
        self.__max_steps = max_steps

    def config_obstacles(self, path: str):
        success = self.__grid._config_obstacles(path)
        self.__screen.set_obstacles(self.__grid.get_obstacles())
        return success

    def _save_log_data(self, path: str, distance_list: List[float],
                       x_distance_list: List[float], y_distance_list: List[float],
                       z_distance_list: List[float], average_time_to_leave: float,
                       y_cross_count_list: List[float]):
        data = {
            "distance": distance_list,
            "x_distance": x_distance_list,
            "y_distance": y_distance_list,
            "z_distance": z_distance_list,
            "time_to_leave": average_time_to_leave,
            "y_cross_count_list": y_cross_count_list,
        }

        with open(path, "w") as f:
            json.dump(data, f)

    def simulate(self, walker: Walker, event: Event, progress_var: DoubleVar, visual=False, graph_output_path:str=None):
        distance_list = [0] * self.__max_steps
        x_distance_list = [0] * self.__max_steps
        y_distance_list = [0] * self.__max_steps
        z_distance_list = [0] * self.__max_steps
        average_time_to_leave = 0
        y_cross_count_list = [0] * self.__max_steps
        
        self.__screen.add_walker(walker)

        for simulation in range(self.__simulation_count):
            self.__screen.reset_trail(walker)
            walker.reset()
            progress_var.set(float(simulation) / self.__simulation_count)

            cross_count = 0
            sign = 0
            time_to_leave = -1

            for step in range(self.__max_steps):
                if event.is_set():
                    break
                if visual:
                    time.sleep(0.00001)

                self.__grid.move(walker)

                location = walker.get_location()
                distance = np.linalg.norm(location)
                # tracking  y axis crosses
                if location[1] - self.__EPSILON > 0:
                    if sign == -1:
                        cross_count += 1
                    sign = 1
                if location[1] + self.__EPSILON < 0:
                    if sign == 1:
                        cross_count += 1
                    sign = -1
                y_cross_count_list[step] += cross_count / float(self.__max_steps)
                # tracking time to leave
                if time_to_leave == -1 and distance > self.__LEAVE_DISTANCE:
                    time_to_leave = step + 1

                distance_list[step] += distance / float(self.__max_steps)
                x_distance_list[step] += location[0] / float(self.__max_steps)
                y_distance_list[step] += location[1] / float(self.__max_steps)
                z_distance_list[step] += location[2] / float(self.__max_steps)

                self.__screen.add_to_trail(walker, walker.get_location())
                

            average_time_to_leave += time_to_leave / float(self.__max_steps)
            
            if event.is_set():
                break

        self.__screen.remove_walker(walker)

        log_path = f"{self.__LOGS_FOLDER}{walker.get_name()}.json"
        self._save_log_data(log_path, distance_list, x_distance_list,
                            y_distance_list, z_distance_list,
                            average_time_to_leave, y_cross_count_list)
        
        if graph_output_path:
            self.generate_graphs(log_path, graph_output_path)

    def run_visual(self, event: Event):
        self.__screen.run(event)
        
    def stop(self):
        self.__screen.stop()

    def generate_graphs(self, log_path: str, output_path: str):
        graph.distance_graph(log_path, output_path)
