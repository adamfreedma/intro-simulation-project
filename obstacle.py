from custom_types import *
from move import Move
import numpy as np


class Obstacle(object):

    def __init__(self, location: vector3, radius: float) -> None:
        self.__location = location
        self.__radius = radius

    def detect_colision(
        self, starting_location: vector3, final_location: vector3
    ) -> bool:
        movement = np.subtract(final_location, starting_location)
        obstacle_to_start = np.subtract(starting_location, self.__location)
        # completely inside
        if np.linalg.norm(obstacle_to_start) < self.__radius: # type: ignore[no-untyped-call]
            return True
        
        coef_a = np.dot(movement, movement) # type: ignore[no-untyped-call]
        coef_b = 2 * np.dot(obstacle_to_start, movement) # type: ignore[no-untyped-call]
        coef_c = np.dot(obstacle_to_start, obstacle_to_start) - self.__radius**2 # type: ignore[no-untyped-call]

        discriminant = coef_b**2 - 4 * coef_a * coef_c
        # no intersection
        if discriminant < 0:
            return False
        else:
            discriminant = np.sqrt(discriminant)

            # cheking to see if the solutions are on the movement part of the line
            solution_1 = (-coef_b - discriminant) / (2 * coef_a)
            solution_2 = (-coef_b + discriminant) / (2 * coef_a)

            solution_1_touched = bool(solution_1 >= 0 and solution_1 <= 1)
            solution_2_touched = bool(solution_2 >= 0 and solution_2 <= 1)
            completely_inside = bool(solution_1 < 0 and solution_2 > 1)

            return solution_1_touched or solution_2_touched or completely_inside

    def get_location(self) -> vector3:
        return self.__location

    def get_radius(self) -> float:
        return self.__radius
