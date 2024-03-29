import json
from teleporter import Teleporter
from obstacle import Obstacle
from speed_zone import SpeedZone
from typing import List
from walker import Walker
from move import Move
import math_functions
import math
from custom_types import *
import os
import numpy as np
import copy
from typing import Optional


class Grid(object):

    __GRAVITY_CONSTANT = 1

    def __init__(self) -> None:
        """
        Initializes a new instance of the Grid class.
        """
        self._obstacles: List[Obstacle] = []

    def clear_obstacles(self) -> None:
        """
        Clears all obstacles from the grid.
        """
        self._obstacles = []

    def add_teleporters(self, path: str) -> bool:
        """
        Adds teleporters to the grid based on the provided config file.

        Args:
            path (str): The path to the config file containing teleporter data.

        Returns:
            bool: True if the teleporters were successfully added, False otherwise.
        """
        teleporter_list = []
        success = False
        # check if the file exists
        if os.path.exists(path):
            success = True
            try:
                with open(path, "rb") as f:
                    data = json.load(f)
                    # add each teleporter to the list based on the correct format
                    for teleporter in data["teleporters"]:
                        teleporter_list.append(
                            Teleporter(
                                teleporter["location"],
                                teleporter["radius"],
                                teleporter["target"],
                            )
                        )
            except KeyError:
                success = False

        # return the success of the operation
        if success:
            self._obstacles.extend(teleporter_list)
        return success

    def add_obstacles(self, path: str) -> bool:
        """
        Adds obstacles to the grid from a config file.

        Args:
            path (str): The path to the config file containing obstacle data.

        Returns:
            bool: True if the obstacles were successfully added, False otherwise.
        """
        obstacle_list = []
        success = False
        # check if the file exists
        if os.path.exists(path):
            success = True
            try:
                with open(path, "rb") as f:
                    data = json.load(f)
                    # add each obstacle to the list based on the correct format
                    for obstacle in data["obstacles"]:
                        obstacle_list.append(
                            Obstacle(obstacle["location"], obstacle["radius"])
                        )
            except KeyError:
                success = False

        # return the success of the operation
        if success:
            self._obstacles.extend(obstacle_list)
        return success

    def add_speed_zones(self, path: str) -> bool:
        """
        Adds speed zones to the grid based on the data provided in a config file.

        Args:
            path (str): The path to the config file containing the speed zone data.

        Returns:
            bool: True if the speed zones were successfully added, False otherwise.
        """
        speed_zone_list = []
        success = False
        # check if the file exists
        if os.path.exists(path):
            success = True
            try:
                with open(path, "rb") as f:
                    data = json.load(f)
                    # add each speed zone to the list based on the correct format
                    for speed_zone in data["speed zones"]:
                        speed_zone_list.append(
                            SpeedZone(
                                speed_zone["location"],
                                speed_zone["radius"],
                                speed_zone["speed factor"],
                            )
                        )
            except KeyError:
                success = False
        # return the success of the operation
        if success:
            self._obstacles.extend(speed_zone_list)
        return success

    def find_closest(
        self, obstacles: List[Obstacle], starting_location: vector3
    ) -> Optional[Obstacle]:
        """
        Finds the closest obstacle to the starting location among the given list of obstacles.

        Args:
            obstacles (List[Obstacle]): A list of obstacles to search through.
            starting_location (vector3): The starting location to measure the distance from.

        Returns:
            Optional[Obstacle]: The closest obstacle to the starting location, or None if no obstacles are provided.

        """
        min_dist = math.inf
        closest = None

        for obstacle in obstacles:
            # get the distance from the starting location to the obstacle
            dist = (
                math_functions.dist(obstacle.get_location(), starting_location)
                - obstacle.get_radius()
            )
            # updates the closest distance
            if dist < min_dist:
                min_dist = dist
                closest = obstacle

        return closest

    def get_gravity_effect(self, walker: Walker, walker_list: List[Walker]) -> Move:
        """
        Calculates the gravity effect on a given walker based on the other walkers in the list.

        Args:
            walker (Walker): The walker for which to calculate the gravity effect.
            walker_list (List[Walker]): The list of other walkers.

        Returns:
            Move: The resulting move representing the gravity effect.

        """
        addition_sum = np.array((0, 0, 0), np.float64)
        total_mass = sum([other_walker.get_mass() for other_walker in walker_list])
        # if gravity should be affecting
        if walker.get_mass() > 0:
            for other_walker in walker_list:
                if other_walker != walker:
                    # calculating the gravity effect
                    distance = math_functions.dist(
                        walker.get_location(), other_walker.get_location()
                    )
                    walker_to_other_walker = np.subtract(
                        other_walker.get_location(), walker.get_location()
                    )
                    direction = math_functions.normalize(
                        cast_to_vector3(walker_to_other_walker)
                    )
                    addition = cast_to_vector3(
                        (
                            np.array(direction)
                            * other_walker.get_mass()
                            * self.__GRAVITY_CONSTANT
                        )
                        / (max(distance, 1) * total_mass)
                    )
                    # adding the gravity effect to the total move
                    addition_sum += addition

        return Move(
            *math_functions.angle_and_radius_from_vector(cast_to_vector3(addition_sum))
        )

    def move(
        self,
        walker: Walker,
        move: Move,
        walker_list: List[Walker],
        obstacles: Optional[List[Obstacle]] = None,
    ) -> None:
        """
        Moves the walker according to the given move and handles collisions with obstacles.

        Args:
            walker (Walker): The walker object to move.
            move (Move): The move to apply to the walker.
            walker_list (List[Walker]): A list of all walkers in the grid.
            obstacles (Optional[List[Obstacle]]): The remaining obstacles, if not provided it will use all of the obstacles in the grid.

        Returns:
            None
        """
        # calculating the uninterrupted move
        starting_location = walker.get_location()
        walker.move(move)
        final_location = walker.get_location()

        if obstacles is None:
            obstacles = copy.deepcopy(self._obstacles)

        # getting all hit obstacles
        hit_obstacles = [
            obstacle
            for obstacle in obstacles
            if obstacle.detect_colision(starting_location, final_location)
        ]
        # finding the closest hit
        closest_hit = self.find_closest(hit_obstacles, starting_location)

        if closest_hit:
            # performing an action based on the type of obstacle hit
            obstacles.remove(closest_hit)
            if type(closest_hit) == SpeedZone:
                walker.move_to(starting_location)
                scaled_move = move
                scaled_move.scale_radius(closest_hit.get_speed_factor())
                self.move(walker, scaled_move, walker_list, obstacles)
            if type(closest_hit) == Teleporter:
                walker.move_to(closest_hit.get_target())
            elif type(closest_hit) == Obstacle:
                walker.move_to(starting_location)
        walker.move(self.get_gravity_effect(walker, walker_list))

    def get_obstacles(self) -> List[Obstacle]:
        """
        Returns a list of obstacles in the grid.

        Returns:
            List[Obstacle]: A list of obstacles in the grid.
        """
        return self._obstacles

    def set_obstacles(self, obstacles: List[Obstacle]) -> None:
        """
        Sets the obstacles on the grid.

        Args:
            obstacles (List[Obstacle]): A list of obstacles to be set on the grid.
        """
        self._obstacles = obstacles
