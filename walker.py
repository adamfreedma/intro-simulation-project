from abc import ABC, abstractmethod
from move import Move
from custom_types import *
import math_functions


class Walker(ABC):

    def __init__(self, name: str, mass: float=1) -> None:
        super().__init__()
        
        self.__name = name
        self.__mass = mass

        self._location = (0, 0, 0)
        self._is_3d: bool

    @abstractmethod
    def _generate_move_radius(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def _generate_move_angle(self) -> Tuple[float, float]:
        raise NotImplementedError

    def get_move(self) -> Move:
        angle = self._generate_move_angle()
        return Move(angle[0], self._generate_move_radius(), angle[1])

    def get_name(self) -> str:
        return self.__name
    
    def get_mass(self) -> float:
        return self.__mass
    
    def is_3d(self) -> bool:
        return self._is_3d

    def get_location(self):
        return self._location

    def move(self, move: Move):
        self._location = math_functions.add_move(self._location, move)

    def move_to(self, location: vector3):
        self._location = location

    def reset(self):
        self._location = (0, 0, 0)
