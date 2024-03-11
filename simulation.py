from grid import Grid
from walker import Walker
import numpy as np
import json
import graph
from screen import Screen
import time
from threading import Event


class Simulation:

    __LEAVE_DISTANCE = 10
    __EPSILON = 0.0001

    def __init__(
        self,
        grid: Grid,
        screen: Screen,
        output_path: str,
        simulation_count=500,
        max_steps=500,
    ) -> None:
        self.__grid = grid
        self.__screen = screen
        self.__output_path = output_path
        self.__simulation_count = simulation_count
        self.__max_steps = max_steps

    def _init_log_data(self):
        self.__distance_list = [0] * self.__max_steps
        self.__x_distance_list = [0] * self.__max_steps
        self.__y_distance_list = [0] * self.__max_steps
        self.__z_distance_list = [0] * self.__max_steps
        self.__average_time_to_leave = 0
        self.__y_cross_count_list = [0] * self.__max_steps

    def config_teleporters(self, path: str):
        success = self.__grid._config_teleporters(path)
        self.__screen.set_teleporters(self.__grid.get_teleporters())
        return success

    def config_obstacles(self, path: str):
        success = self.__grid._config_obstacles(path)
        self.__screen.set_obstacles(self.__grid.get_obstacles())
        return success

    def _save_log_data(self):
        data = {
            "distance": self.__distance_list,
            "x_distance": self.__x_distance_list,
            "y_distance": self.__y_distance_list,
            "z_distance": self.__z_distance_list,
            "time_to_leave": self.__average_time_to_leave,
            "y_cross_count_list": self.__y_cross_count_list,
        }

        with open(self.__output_path, "w") as f:
            json.dump(data, f)

    def simulate(self, walker: Walker, event: Event):
        self._init_log_data()
        self.__screen.add_walker(walker)

        for simulation in range(self.__simulation_count):
            self.__screen.reset_trail(walker)
            walker.reset()

            cross_count = 0
            sign = 0
            time_to_leave = -1

            for step in range(self.__max_steps):
                if event.is_set():
                    break

                self.__grid.move(walker)
                time.sleep(0.00001)

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
                self.__y_cross_count_list[step] += cross_count / float(self.__max_steps)
                # tracking time to leave
                if time_to_leave == -1 and distance > self.__LEAVE_DISTANCE:
                    time_to_leave = step + 1

                self.__distance_list[step] += distance / float(self.__max_steps)
                self.__x_distance_list[step] += location[0] / float(self.__max_steps)
                self.__y_distance_list[step] += location[1] / float(self.__max_steps)
                self.__z_distance_list[step] += location[2] / float(self.__max_steps)

                self.__screen.add_to_trail(walker, walker.get_location())

            self.__average_time_to_leave += time_to_leave / float(self.__max_steps)
            if event.is_set():
                break

        self.__screen.remove_walker(walker)

        self._save_log_data()

    def run_visual(self, event: Event):
        self.__screen.run(event)

    def graph(self):
        graph.distance_graph(self.__output_path)
