from grid import Grid
from walker import Walker
import numpy as np
import json
import graph

class Simulation:

    __LEAVE_DISTANCE = 10
    __EPSILON = 0.0001

    def __init__(
        self, grid: Grid, output_path: str, simulation_count=500, max_steps=500
    ) -> None:
        self.__grid = grid
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

    def _save_log_data(self):
        data = {
            "distance": self.__distance_list,
            "x_distance": self.__x_distance_list,
            "y_distance": self.__y_distance_list,
            "z_distance": self.__z_distance_list,
            "time_to_leave": self.__average_time_to_leave,
            "y_cross_count_list": self.__y_cross_count_list,
        }
        
        with open(self.__output_path, 'w') as f:
            json.dump(data, f)

    def simulate(self, walker: Walker):
        self._init_log_data()

        for simultaion in range(self.__simulation_count):
            walker.reset()

            cross_count = 0
            sign = 0
            time_to_leave = -1

            for step in range(self.__max_steps):
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
                self.__y_cross_count_list[step] += cross_count / float(self.__max_steps)
                # tracking time to leave
                if time_to_leave == -1 and distance > self.__LEAVE_DISTANCE:
                    time_to_leave = step + 1

                if distance != 1 and step == 0:
                    print("ahhhhh")

                self.__distance_list[step] += distance / float(self.__max_steps)
                self.__x_distance_list[step] += location[0] / float(self.__max_steps)
                self.__y_distance_list[step] += location[1] / float(self.__max_steps)
                self.__z_distance_list[step] += location[2] / float(self.__max_steps)

            self.__average_time_to_leave += time_to_leave / float(self.__max_steps)

        self._save_log_data()
        
    def graph(self):
        graph.distance_graph(self.__output_path)