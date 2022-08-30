from schemas.pizzabase import PizzaBase


def test_check_default_values() -> None:
    pizzabase = PizzaBase(name="base")
    assert pizzabase.fuel_amount == 1000


def test_2() -> None:
    pizzabase = PizzaBase(name="base")
    assert pizzabase.pk == 0

    pizzabase2 = PizzaBase(name="base2")
    assert pizzabase2.pk == 0
