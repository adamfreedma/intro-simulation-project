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
        super().__init__(location, radius)
        self.__speed_factor = speed_factor

    def get_speed_factor(self) -> float:
        return self.__speed_factor
    
    def get_color(self) -> vector3:
        value = 0.5
        
        if self.__speed_factor > 1:
            value = 0.5 + min(((self.__speed_factor * self.__COLOR_FADE_SPEED - 1) / (2 * self.__speed_factor * self.__COLOR_FADE_SPEED)), 0.5)
        if self.__speed_factor < 1:
            value = 0.5 - min((1 - self.__speed_factor / self.__COLOR_FADE_SPEED) / 2, 0.5)
            
        return (min(2 * (1 - value), 1), min(2 * value, 1), 0)
        