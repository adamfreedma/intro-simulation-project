from walker import Walker
import math_functions
import random
from custom_types import *
from typing import Tuple

class RandomWalker(Walker):

    def __init__(self, name: str, is_3d: bool, mass: float=1) -> None:
        """
        Initialize a RandomWalker object.

        Args:
            name (str): The name of the random walker.
            is_3d (bool): A flag indicating whether the random walker is in 3D or not.
            mass (float, optional): The mass of the random walker. Defaults to 1.
        """
        super().__init__(name, mass)

        self._is_3d = is_3d

    def _generate_move_radius(self) -> float:
        """
        Generates a random move radius for the walker.

        Returns:
            float: The generated move radius.
        """
        return 0.5 + random.random()

    def _generate_move_angle(self) -> Tuple[float, float]:
        """
        Generates a random move angle for the walker.

        Returns:
            tuple: A tuple containing the move angles. If the walker is in 3D, the tuple contains two random angles.
            If the walker is in 2D, the tuple contains one random angle and 0.0 for the second angle.
        """
        result = None
        if self._is_3d:
            result = (math_functions.random_angle(), math_functions.random_angle())
        else:
            result = (math_functions.random_angle(), 0.0)

        return result
