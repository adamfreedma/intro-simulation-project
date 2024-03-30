from abc import ABC, abstractmethod
from move import Move
from custom_types import *
from math_functions import MathFunctions
from typing import Tuple


class Walker(ABC):

    def __init__(self, name: str, mass: float = 1) -> None:
        """
        Initialize a Walker object.

        Args:
            name (str): The name of the walker.
            mass (float, optional): The mass of the walker. Defaults to 1.
        """
        super().__init__()

        self._name = name
        self._mass = mass

        self._location = (0.0, 0.0, 0.0)
        self._is_3d: bool

    @abstractmethod
    def _generate_move_radius(self) -> float:
        """
        Generates a random move radius for the walker.

        Returns:
            float: The randomly generated move radius.
        """
        raise NotImplementedError

    @abstractmethod
    def _generate_move_angle(self) -> Tuple[float, float]:
        """
        Generates a random move angle for the walker.

        Returns:
            tuple: A tuple containing two float values representing the move angle.
        """
        raise NotImplementedError

    def get_move(self) -> Move:
        """
        Generates a random move for the walker.

        Returns:
            Move: A Move object representing the generated move.
        """
        angle = self._generate_move_angle()
        return Move(angle[0], self._generate_move_radius(), angle[1])

    def get_name(self) -> str:
        """
        Returns the name of the walker.

        Returns:
            str: The name of the walker.
        """
        return self._name

    def get_mass(self) -> float:
        """
        Returns the mass of the walker.

        Returns:
            float: The mass of the walker.
        """
        return self._mass

    def is_3d(self) -> bool:
        """
        Returns True if the walker is in a 3D environment, False otherwise.

        Returns:
            bool: is the walker in a 3D environment?
        """
        return self._is_3d

    def get_location(self) -> Types.vector3:
        return self._location

    def move(self, move: Move) -> None:
        self._location = MathFunctions.add_move(self._location, move)

    def move_to(self, location: Types.vector3) -> None:
        self._location = location

    def reset(self) -> None:
        self._location = (0, 0, 0)
