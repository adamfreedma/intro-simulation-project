import json
from teleporter import Teleporter
from obstacle import Obstacle
from typing import List


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