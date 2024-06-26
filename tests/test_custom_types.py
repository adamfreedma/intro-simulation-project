from custom_types import Types


def test_cast_to_vector3() -> None:
    # Test invalid input with less than 3 components
    valueError = False
    try:
        Types.cast_to_vector3([1.0, 2.0])
    except ValueError as e:
        valueError = str(e) == "Vector3 must have 3 components"
    assert valueError, "Expected ValueError"
