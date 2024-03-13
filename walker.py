from abc import ABC, abstractmethod
from move import Move
from custom_types import *
import math_functions


class Walker(ABC):

    def __init__(self, name: str) -> None:
        super().__init__()
        
        self.__name = name

        self.__location = (0, 0, 0)
        self.__is_3d: bool

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

    def get_location(self):
        return self.__location

    def move(self, move: Move):
        self.__location = math_functions.add_move(self.__location, move)

    def move_to(self, location: vector3):
        self.__location = location

    def reset(self):
        self.__location = (0, 0, 0)
