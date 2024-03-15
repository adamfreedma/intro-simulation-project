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

class Grid(object):

    def __init__(self) -> None:
        self._obstacles = []

    def clear_obstacles(self):
        self._obstacles = []

    def _add_teleporters(self, path: str) -> bool:
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
            self._obstacles.extend(teleporter_list)
        return success

    def _add_obstacles(self, path: str) -> bool:
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
            self._obstacles.extend(obstacle_list)
        return success

    def _add_speed_zones(self, path: str) -> bool:
        speed_zone_list = []
        success = False

        if os.path.exists(path):
            success = True
            try:
                with open(path, "rb") as f:
                    data = json.load(f)

                    for speed_zone in data["speed zones"]:
                        speed_zone_list.append(
                            SpeedZone(speed_zone["location"], speed_zone["radius"], speed_zone["speed factor"])
                        )
            except KeyError:
                success = False

        if success:
            self._obstacles.extend(speed_zone_list)
        return success

    def find_closest(
        self, obstacles: List[Obstacle], starting_location: vector3
    ) -> Obstacle:
        min_dist = math.inf
        closest = None

        for obstacle in obstacles:
            dist = math_functions.dist(obstacle.get_location(), starting_location) - obstacle.get_radius()
            if dist < min_dist:
                min_dist = dist
                closest = obstacle

        return closest

    def move(self, walker: Walker, move: Move, obstacles: List[Obstacle]=None):
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

        closest_hit = self.find_closest(hit_obstacles, starting_location)

        if closest_hit:
            obstacles.remove(closest_hit)
            if type(closest_hit) == SpeedZone:
                walker.move_to(starting_location)
                scaled_move = move
                scaled_move.scale_radius(closest_hit.get_speed_factor())
                self.move(walker, scaled_move, obstacles)
            if type(closest_hit) == Teleporter:
                walker.move_to(closest_hit.get_target())
            elif type(closest_hit) == Obstacle:
                walker.move_to(starting_location)

    def get_obstacles(self) -> List[Obstacle]:
        return self._obstacles
