from typing import Any, Tuple


class Types:
    
    vector3 = Tuple[float, float, float]
    angle_vector3 = Tuple[float, float, float]

    def cast_to_vector3(value: Any) -> vector3:
        """
        Casts a value to a vector3.

        Args:
            value (Any): The value to be casted to a vector3.

        Returns:
            vector3: The casted vector3.

        Raises:
            ValueError: If the value does not have 3 components.
        """
        try:
            return (value[0], value[1], value[2])
        except IndexError:
            raise ValueError("Vector3 must have 3 components")
