from walker import Walker
import math_functions
from custom_types import *
import math
from typing import Tuple, Callable, Dict


class AcceleratingWalker(Walker):

    __ACCELERATION_SCALE = 0.1
    ACCELERATION_TYPES: Dict[str, Callable[[float], float]] = {
        "Linear": lambda x: AcceleratingWalker.__ACCELERATION_SCALE * x,
        "Quadratic": lambda x: math.pow(AcceleratingWalker.__ACCELERATION_SCALE * x, 2),
        "Logarithmic": lambda x: math.log(AcceleratingWalker.__ACCELERATION_SCALE * x),
        "Square Root": lambda x: math.sqrt(AcceleratingWalker.__ACCELERATION_SCALE * x),
    }

    def __init__(
        self, name: str, is_3d: bool, mass: float = 1, acceleration_type: str = "Linear"
    ) -> None:
        """Constructor for AcceleratingWalker

        Args:
            name (str): walker's name
            is_3d (bool): is the walker in 3D
            mass (float, optional): walker's mass. Defaults to 1.
            acceleration_type (str, optional): acceleration type. Defaults to "Linear".
        """
        super().__init__(name, mass)

        self._is_3d = is_3d
        self.__step = 0
        # updating acceleration type
        if acceleration_type in AcceleratingWalker.ACCELERATION_TYPES:
            self.__acceleration_type = acceleration_type
        else:
            self.__acceleration_type = "Linear"

    def _generate_move_radius(self) -> float:
        """
        Generates the move radius based on the current step and acceleration type.

        Returns:
            float: The move radius for the current step.
        """
        self.__step = self.__step + 1
        return self.ACCELERATION_TYPES[self.__acceleration_type](self.__step)

    def _generate_move_angle(self) -> Tuple[float, float]:
        """
        Generates a random move angle for the walker.

        Returns:
            tuple: A tuple of two floats representing the move angles. If the walker is in 3D, both angles are random.
            If the walker is in 2D, the first angle is random and the second angle is 0.0.
        """
        result = None
        if self._is_3d:
            result = (math_functions.random_angle(), math_functions.random_angle())
        else:
            result = (math_functions.random_angle(), 0.0)

        return result

    def reset(self) -> None:
        """
        Resets the state of the walker and sets the step count to 0.
        """
        self.__step = 0
        super().reset()

    def get_acceleration_type(self) -> str:
        """
        Returns the acceleration type of the walker.

        Returns:
            str: The acceleration type of the walker.
        """
        return self.__acceleration_type
