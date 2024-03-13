from walker import Walker
import math_functions
from custom_types import *
import math
import numpy as np


class BiasedWalker(Walker):

    __BIAS_DICT = {
        "L": (-0.5 * math.pi, 0),
        "R": (0.5 * math.pi, 0),
        "F": (0, 0),
        "B": (math.pi, 0),
        "U": (0, 0.5 * math.pi),
        "D": (0, -0.5 * math.pi),
    }

    def __init__(self, name: str, is_3d: bool, bias: str, bias_scale=1) -> None:
        super().__init__(name)

        self._is_3d = is_3d
        self.bias = bias
        self.bias_scale = bias_scale

    def _generate_move_radius(self) -> float:
        return 1

    def _generate_move_angle(self) -> Tuple[float, float]:
        result = None

        # generating a normally distributed change in angle from the bias direction
        change_direction = math_functions.random_angle()
        changee_magnitude = np.random.normal(scale=self.bias_scale)  # change in radians

        # finding the bias direction from the bias dictionary
        if self.bias in self.__BIAS_DICT:
            yaw, pitch = self.__BIAS_DICT[self.bias]
        # finding the bias direction as the opposite of the current location
        elif self.bias == "O":
            yaw = math.atan2(self._location[1], self._location[0])
            pitch = (
                math.atan2(self._location[2], np.linalg.norm(self._location[:2]))
                + math.pi
            )

        if self._is_3d:
            # adding the yaw and pitch change partially to both axis
            new_yaw = yaw + math.cos(change_direction) * changee_magnitude
            new_pitch = pitch + math.sin(change_direction) * changee_magnitude

            result = (new_yaw, new_pitch)
        else:
            # adding the yaw change
            result = (yaw + changee_magnitude + math.pi, 0)

        return result
