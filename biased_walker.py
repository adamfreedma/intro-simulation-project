from walker import Walker
import math_functions
from custom_types import *
import math
import numpy as np
import random
from typing import Tuple

class BiasedWalker(Walker):

    BIAS_DICT = {
        "Left": (0.5 * math.pi, 0),
        "Right": (-0.5 * math.pi, 0),
        "Front": (0, 0),
        "Back": (math.pi, 0),
        "Up": (0, 0.5 * math.pi),
        "Down": (0, -0.5 * math.pi),
    }

    def __init__(self, name: str, is_3d: bool, mass: float=1.0, bias: str="", bias_scale: int=1) -> None:
        """
        Initialize a BiasedWalker object.

        Args:
            name (str): The name of the walker.
            is_3d (bool): A flag indicating whether the walker is in 3D or not.
            mass (float, optional): The mass of the walker. Defaults to 1.0.
            bias (str, optional): The bias of the walker. Defaults to an empty string.
            bias_scale (int, optional): The scale of the bias. Defaults to 1.

        Returns:
            None
        """
        super().__init__(name, mass)

        self._is_3d = is_3d
        self.bias_scale = bias_scale
        if bias in self.BIAS_DICT or bias == "Origin":
            self.bias = bias
        else:
            self.bias = random.choice(list(self.BIAS_DICT.keys()))


    def _generate_move_radius(self) -> float:
        """
        Generates the radius for a move.

        Returns:
            float: The generated move radius.
        """
        return 1.0

    def _generate_move_angle(self) -> Tuple[float, float]:
        """
        Generates a move angle based on the bias direction and bias scale.

        Returns:
            tuple: A tuple containing the new yaw and pitch angles.
        """
        result = None

        # generating a normally distributed change in angle from the bias direction
        change_direction = math_functions.random_angle()
        changee_magnitude = np.random.normal(scale=self.bias_scale)  # change in radians

        # finding the bias direction from the bias dictionary
        if self.bias in self.BIAS_DICT:
            yaw, pitch = self.BIAS_DICT[self.bias]
        # finding the bias direction as the opposite of the current location
        elif self.bias == "Origin":
            yaw = math.atan2(self._location[1], self._location[0])
            pitch = (math.atan2(self._location[2], np.linalg.norm(self._location[:2])) # type: ignore[no-untyped-call]
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

        return (result[0] % (2 * math.pi), result[1] % (2 * math.pi))
