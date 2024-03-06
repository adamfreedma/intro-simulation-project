from walker import Walker
import math_functions
from custom_types import *

class RandomAngleWalker(Walker):
    
    def _generate_move_radius(self) -> float:
        return 1
    
    def _generate_move_angle(self, is_3d=False) -> Tuple[float, float]:
        result = None
        if is_3d:
            result = (math_functions.random_angle(), math_functions.random_angle())
        else:
            result = (math_functions.random_angle(), 0)
            
        return result
