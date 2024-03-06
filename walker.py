from abc import ABC, abstractmethod 
from move import Move
from custom_types import *
import math_functions

class Walker(ABC):
    
    _location = (0, 0, 0)
        
    @abstractmethod
    def _generate_move_radius(self) -> float:
        raise NotImplementedError
    
    
    @abstractmethod
    def _generate_move_angle(self, is_3d=False) -> Tuple[float, float]:
        raise NotImplementedError

    
    def get_move(self, is_3d=False) -> Move:
        angle = self._generate_move_angle(is_3d)
        return Move(angle[0], self._generate_move_radius(), angle[1])

    def get_location(self):
        return self._location
    
    def move(self, is_3d=False):
        self._location = math_functions.add_move(self._location, self.get_move())
        
    def reset(self):
        self._location = (0, 0, 0)