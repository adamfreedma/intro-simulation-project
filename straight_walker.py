import re
from walker import Walker
from custom_types import *
import math
import random
from typing import Tuple


class StraightWalker(Walker):

    def __init__(self, name: str, is_3d: bool, mass: float = 1) -> None:
        """
        Initialize a StraightWalker object.

        Args:
            name (str): The name of the walker.
            is_3d (bool): Indicates whether the walker is in 3D or not.
            mass (float, optional): The mass of the walker. Defaults to 1.
        """
        super().__init__(name, mass)

        self._is_3d = is_3d

    def _generate_move_radius(self) -> float:
        """
        Generates a random move radius for the walker.

        Returns:
            float: The generated move radius.
        """
        return 1.0

    def _generate_move_angle(self) -> Tuple[float, float]:
        """
        Generates a random move angle for the walker.

        Returns:
            A tuple containing two float values representing the move angle.
            The first value represents the yaw, The second value represents the pitch.
        """
        result = (0.0, 0.0)
        if self._is_3d:
            # choosing a random yaw and pitch
            random_int = random.randint(0, 5)
            if random_int >= 4:
                result = (0, (random_int - 4.5) * math.pi)
            else:
                result = (random_int * math.pi / 2, 0.0)
        else:
            # choosing a random yaw
            result = (random.randint(0, 3) * math.pi / 2, 0.0)

        return (result[0] % (2 * math.pi), result[1] % (2 * math.pi))
