from walker import Walker
from custom_types import *
import math
import random
from typing import Tuple

class StraightWalker(Walker):

    def __init__(self, name: str, is_3d: bool, mass: float=1) -> None:
        super().__init__(name, mass)

        self._is_3d = is_3d

    def _generate_move_radius(self) -> float:
        return 1

    def _generate_move_angle(self) -> Tuple[float, float]:
        result = (0.0, 0.0)
        if self._is_3d:
            random_int = random.randint(0, 5)
            if random_int >= 4:
                result = (0, (random_int - 4.5) * math.pi)
            else:
                result = (random_int * math.pi / 2, 0)
        else:
            result = (random.randint(0, 3) * math.pi / 2, 0)

        return result
