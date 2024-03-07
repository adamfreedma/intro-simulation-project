from custom_types import *
from move import Move
import numpy as np

class Obstacle(object):
    
    def __init__(self, location: vector3, radius: float) -> None:
        self.__location = location
        self.__radius = radius
        
    def detect_colision(self, starting_location: vector3, final_location: vector3) -> bool:
        movement = np.subtract(final_location, starting_location)
        teleporter_to_start = np.subtract(starting_location, self.__location)
        coef_a = np.dot(movement, movement)
        coef_b = 2 * np.dot(teleporter_to_start, movement)
        coef_c = np.dot(teleporter_to_start, teleporter_to_start) - self.__radius ** 2

        discriminant = coef_b**2-4*coef_a*coef_c;
        # no intersection
        if discriminant < 0: 
            return False
        else:
            discriminant = np.sqrt(discriminant)

            # cheking to see if the solutions are on the movement part of the line
            solution_1 = (-coef_b - discriminant)/(2*coef_a);
            solution_2 = (-coef_b + discriminant)/(2*coef_a);
    
            solution_1_touched = solution_1 >= 0 and solution_1 <= 1
            solution_2_touched = solution_2 >= 0 and solution_2 <= 1
            completly_inside = solution_1 < 0 and solution_2 > 1
    
            return solution_1_touched or solution_2_touched or completly_inside
    