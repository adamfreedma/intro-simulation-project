from walker import Walker
import math_functions
import random
from custom_types import *
from typing import Tuple

class RandomWalker(Walker):

    def __init__(self, name: str, is_3d: bool, mass: float=1) -> None:
        super().__init__(name, mass)

        self._is_3d = is_3d

    def _generate_move_radius(self) -> float:
        return 0.5 + random.random()

    def _generate_move_angle(self) -> Tuple[float, float]:
        result = None
        if self._is_3d:
            result = (math_functions.random_angle(), math_functions.random_angle())
        else:
            result = (math_functions.random_angle(), 0.0)

        return result
