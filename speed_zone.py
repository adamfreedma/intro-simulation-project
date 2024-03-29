from custom_types import *
from custom_types import vector3
from obstacle import Obstacle
from typing import Tuple


class SpeedZone(Obstacle):

    __COLOR_FADE_SPEED = 0.5

    def __init__(
        self,
        location: Tuple[float, float, float],
        radius: float,
        speed_factor: float,
    ) -> None:
        """
        Initialize a SpeedZone object.

        Args:
            location (Tuple[float, float, float]): The location of the speed zone.
            radius (float): The radius of the speed zone.
            speed_factor (float): The factor by which the speed is multiplied within the speed zone.
        """
        super().__init__(location, radius)
        self.__speed_factor = speed_factor

    def get_speed_factor(self) -> float:
        """
        Returns the speed factor of the speed zone.

        Returns:
            float: The speed factor of the speed zone.
        """
        return self.__speed_factor

    def get_color(self) -> vector3:
        """
        Returns the color of the speed zone based on the speed factor.

        The color is determined by the speed factor, which represents the ratio of the current speed to the maximum speed.
        If the speed factor is greater than 1, the color will fade from yellow to green as the speed increases.
        If the speed factor is less than 1, the color will fade from yellow to red as the speed decreases.

        Returns:
            A tuple representing the RGB color values as floats between 0 and 1.
        """
        value = 0.5

        if self.__speed_factor > 1:
            # fading from yellow to green
            value = 0.5 + min(
                (
                    (self.__speed_factor * self.__COLOR_FADE_SPEED - 1)
                    / (2 * self.__speed_factor * self.__COLOR_FADE_SPEED)
                ),
                0.5,
            )
        if self.__speed_factor < 1:
            # fading from yellow to red
            value = 0.5 - min(
                (1 - self.__speed_factor / self.__COLOR_FADE_SPEED) / 2, 0.5
            )

        return (min(2 * (1 - value), 1), min(2 * value, 1), 0)
