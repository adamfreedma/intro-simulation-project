from walker import Walker
from math_functions import MathFunctions
from custom_types import *
from typing import Tuple


class RandomAngleWalker(Walker):

    def __init__(self, name: str, is_3d: bool, mass: float = 1) -> None:
        """
        Initialize a RandomAngleWalker object.

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
            tuple: A tuple containing the move angles. If the walker is in 3D, the tuple contains two random angles.
            If the walker is in 2D, the tuple contains one random angle and 0.

        """
        result = None
        if self._is_3d:
            result = (MathFunctions.random_angle(), MathFunctions.random_angle())
        else:
            result = (MathFunctions.random_angle(), 0)

        return result
