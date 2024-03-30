from custom_types import *
from move import Move
import numpy as np


class Obstacle(object):

    def __init__(self, location: Types.vector3, radius: float) -> None:
        """
        Initialize an Obstacle object.

        Args:
            location (Types.vector3): The location of the obstacle.
            radius (float): The radius of the obstacle.
        """
        self.__location = location
        self.__radius = radius

    def detect_colision(
        self, starting_location: Types.vector3, final_location: Types.vector3
    ) -> bool:
        """
        Detects whether a collision occurred between the obstacle and a movement from a starting location to a final location.

        Args:
            starting_location (Types.vector3): The starting location of the movement.
            final_location (Types.vector3): The final location of the movement.

        Returns:
            bool: True if there is a collision, False otherwise.
        """
        movement = np.subtract(final_location, starting_location)
        obstacle_to_start = np.subtract(starting_location, self.__location)
        # completely inside
        if np.linalg.norm(obstacle_to_start) < self.__radius:  # type: ignore[no-untyped-call]
            return True
        # finding the coefficients for the quadratic equation
        coef_a = np.dot(movement, movement)  # type: ignore[no-untyped-call]
        coef_b = 2 * np.dot(obstacle_to_start, movement)  # type: ignore[no-untyped-call]
        coef_c = np.dot(obstacle_to_start, obstacle_to_start) - self.__radius**2  # type: ignore[no-untyped-call]

        discriminant = coef_b**2 - 4 * coef_a * coef_c
        if discriminant < 0:
            # no intersection
            return False
        else:
            discriminant = np.sqrt(discriminant)

            # cheking to see if the solutions are on the correct part of the line
            solution_1 = (-coef_b - discriminant) / (2 * coef_a)
            solution_2 = (-coef_b + discriminant) / (2 * coef_a)

            solution_1_touched = bool(solution_1 >= 0 and solution_1 <= 1)
            solution_2_touched = bool(solution_2 >= 0 and solution_2 <= 1)
            completely_inside = bool(solution_1 < 0 and solution_2 > 1)
            # is there a collision
            return solution_1_touched or solution_2_touched or completely_inside

    def get_location(self) -> Types.vector3:
        """
        Returns the location of the obstacle as a Types.vector3 object.

        Returns:
            Types.vector3: The location of the obstacle.
        """
        return self.__location

    def get_radius(self) -> float:
        """
        Returns the radius of the obstacle.

        Returns:
            float: The radius of the obstacle.
        """
        return self.__radius
