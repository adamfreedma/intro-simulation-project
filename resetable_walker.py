from move import Move
from walker import Walker
from math_functions import MathFunctions
from custom_types import *
from typing import Tuple
import random

class ResetableWalker(Walker):

    __RESET_CHANCE_SCALE = 0.1
    
    def __init__(
        self, name: str, is_3d: bool, mass: float = 1) -> None:
        """Constructor for ResetableWalker

        Args:
            name (str): walker's name
            is_3d (bool): is the walker in 3D
            mass (float, optional): walker's mass. Defaults to 1.
        """
        super().__init__(name, mass)

        self._is_3d = is_3d
        self.__step = 1

    def _generate_move_radius(self) -> float:
        """
        Generates the move radius based on the current step and acceleration type.

        Returns:
            float: The move radius for the current step.
        """
        self.__step = self.__step + 1
        return 1.0

    def _generate_move_angle(self) -> Tuple[float, float]:
        """
        Generates a random move angle for the walker.

        Returns:
            tuple: A tuple of two floats representing the move angles. If the walker is in 3D, both angles are random.
            If the walker is in 2D, the first angle is random and the second angle is 0.0.
        """
        result = None
        if self._is_3d:
            result = (MathFunctions.random_angle(), MathFunctions.random_angle())
        else:
            result = (MathFunctions.random_angle(), 0.0)

        return result
    
    def move(self, move: Move) -> None:
        """Calculates the walker's chance to reset and moves the walker.

        Args:
            move (Move): the move to make if the walker doesn't reset
        """
        reset_chance = 1 - 1 / (self.__step * self.__RESET_CHANCE_SCALE)
        if random.random() < reset_chance:
            self.reset()
        else:
            super().move(move)

    def reset(self) -> None:
        """
        Resets the state of the walker and sets the step count to 0.
        """
        self.__step = 1
        super().reset()