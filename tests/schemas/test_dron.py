from schemas.dron import Dron


def test_check_default_values() -> None:
    dron = Dron()
    assert dron.coordinates == (0, 0)
    assert dron.fuel == 25
    assert dron.distance_to_base == 0
    assert dron.next_coordinates == (0, 0)
