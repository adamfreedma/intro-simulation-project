from custom_types import *
from custom_types import vector3
from obstacle import Obstacle


class Teleporter(Obstacle):

    def __init__(
        self,
        location: Tuple[float, float, float],
        radius: float,
        target: Tuple[float, float, float],
    ) -> None:
        super().__init__(location, radius)
        self.__target = target

    def get_target(self) -> vector3:
        return self.__target
