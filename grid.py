import json
from teleporter import Teleporter
from obstacle import Obstacle
from typing import List
from walker import Walker
from move import Move
import math_functions
import math
from custom_types import *
import os
import copy


class Grid(object):

    def __init__(self, obstacles_path="", teleporters_path="") -> None:
        self._obstacles = []
        self._teleporters = []
        self._config_obstacles(obstacles_path)
        self._config_teleporters(teleporters_path)

    def _config_teleporters(self, path: str) -> bool:
        teleporter_list = []
        success = False

        if os.path.exists(path):
            success = True
            try:
                with open(path, "rb") as f:
                    data = json.load(f)

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
        if success:
            self._teleporters = teleporter_list
        return success

    def _config_obstacles(self, path: str) -> bool:
        obstacle_list = []
        success = False

        if os.path.exists(path):
            success = True
            try:
                with open(path, "rb") as f:
                    data = json.load(f)

                    for obstacle in data["obstacles"]:
                        obstacle_list.append(
                            Obstacle(obstacle["location"], obstacle["radius"])
                        )
            except KeyError:
                success = False

        if success:
            self._obstacles = obstacle_list
        return success

    def find_closest(
        self, obstacles: List[Obstacle], starting_location: vector3
    ) -> Obstacle:
        min_dist = math.inf
        closest = None

        for obstacle in obstacles:
            dist = math_functions.dist(obstacle.get_location(), starting_location)
            if dist < min_dist:
                min_dist = dist
                closest = obstacle

        return closest

    def move(self, walker: Walker):
        starting_location = walker.get_location()
        walker.move(walker.get_move())
        final_location = walker.get_location()
        # getting all hit obstacles
        hit_obstacles = [
            obstacle
            for obstacle in self._obstacles
            if obstacle.detect_colision(starting_location, final_location)
        ]
        # getting all hit teleporters
        hit_teleporters = [
            teleporter
            for teleporter in self._teleporters
            if teleporter.detect_colision(starting_location, final_location)
        ]

        closest_hit = self.find_closest(
            set(hit_teleporters + hit_obstacles), starting_location
        )

        if closest_hit:
            if isinstance(closest_hit, Teleporter):
                walker.move_to(closest_hit.get_target())
            elif isinstance(closest_hit, Obstacle):
                walker.move_to(starting_location)

    def get_teleporters(self) -> List[Teleporter]:
        return copy.deepcopy(self._teleporters)

    def get_obstacles(self) -> List[Obstacle]:
        return copy.deepcopy(self._obstacles)
