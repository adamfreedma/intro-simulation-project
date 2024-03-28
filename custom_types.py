from typing import Any, Tuple

vector3 = Tuple[float, float, float]
angle_vector3 = Tuple[float, float, float]

def cast_to_vector3(value: Any) -> vector3:
    try:
        return (value[0], value[1], value[2])
    except IndexError:
        raise ValueError("Vector3 must have 3 components")