from walker import Walker
import math_functions
import random
from custom_types import *

class RandomAngleWalker(Walker):
    
    def __init__(self) -> None:
        super().__init__()
    
    def _generate_move_radius(self) -> float:
        return 0.5 + random.random()
    
    def _generate_move_angle(self, is_3d=False) -> Tuple[float, float]:
        result = None
        if is_3d:
            result = (math_functions.random_angle(), math_functions.random_angle())
        else:
            result = (math_functions.random_angle(), 0)
            
        return result