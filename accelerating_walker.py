from walker import Walker
import math_functions
from custom_types import *
import math
from typing import Tuple, Callable, Dict

class AcceleratingWalker(Walker):

    __ACCELERATION_SCALE = 0.1
    ACCELERATION_TYPES: Dict[str, Callable[[float], float]] = {"Linear": lambda x: AcceleratingWalker.__ACCELERATION_SCALE * x,
                            "Quadratic": lambda x: math.pow(AcceleratingWalker.__ACCELERATION_SCALE * x, 2),
                            "Logarithmic": lambda x: math.log(AcceleratingWalker.__ACCELERATION_SCALE * x),
                            "Square Root": lambda x: math.sqrt(AcceleratingWalker.__ACCELERATION_SCALE * x)
                            }
    

    def __init__(self, name: str, is_3d: bool, mass: float=1, acceleration_type: str="Linear") -> None:
        super().__init__(name, mass)

        self._is_3d = is_3d
        self.__step = 0
        
        if acceleration_type in AcceleratingWalker.ACCELERATION_TYPES:
            self.__acceleration_type = acceleration_type
        else:
            self.__acceleration_type = "Linear"

    def _generate_move_radius(self) -> float:
        self.__step = self.__step + 1
        return self.ACCELERATION_TYPES[self.__acceleration_type](self.__step)

    def _generate_move_angle(self) -> Tuple[float, float]:
        result = None
        if self._is_3d:
            result = (math_functions.random_angle(), math_functions.random_angle())
        else:
            result = (math_functions.random_angle(), 0)

        return result
    
    def reset(self) -> None:
        self.__step = 0
        super().reset()
