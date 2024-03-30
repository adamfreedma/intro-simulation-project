from custom_types import *
from custom_types import Types
from obstacle import Obstacle
from typing import Tuple


class Teleporter(Obstacle):

    def __init__(
        self,
        location: Tuple[float, float, float],
        radius: float,
        target: Tuple[float, float, float],
    ) -> None:
        """
        Initialize a Teleporter object.

        Args:
            location (Tuple[float, float, float]): The location of the teleporter.
            radius (float): The radius of the teleporter.
            target (Tuple[float, float, float]): The target location to teleport to.
        """
        super().__init__(location, radius)
        self.__target = target

    def get_target(self) -> Types.vector3:
        """
        Returns the target location of the teleporter.

        Returns:
            Types.vector3: The target location of the teleporter.
        """
        return self.__target
