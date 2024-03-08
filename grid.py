import json
from teleporter import Teleporter
from obstacle import Obstacle
from typing import List
from walker import Walker
from move import Move
import math_functions
import math
from custom_types import *


class Grid(object):

    def __init__(self, obstacles_path: str, teleporters_path: str) -> None:
        self._obstacles = self._read_obstacles(obstacles_path)
        self._teleporters = self._read_teleporters(teleporters_path)

    def _read_teleporters(self, path: str) -> List[Teleporter]:
        teleporter_list = []

        with open(path, "rb") as f:
            data = json.load(f)

            for teleporter in data:
                teleporter_list.append(
                    Teleporter(
                        teleporter["location"],
                        teleporter["radius"],
                        teleporter["target"],
                    )
                )

        return teleporter_list

    def _read_obstacles(self, path: str) -> List[Obstacle]:
        obstacle_list = []

        with open(path, "rb") as f:
            data = json.load(f)

            for obstacle in data:
                obstacle_list.append(Obstacle(obstacle["location"], obstacle["radius"]))

        return obstacle_list

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
