from typing import List

import pytest
from fixtures.offers import buy_one_apple_get_one_free, half_price_oranges
from pytest_bdd import given, scenario, then, when

from basket import Basket
from catalogue import Catalogue, UnknownPrice
from pricer import Offer, Pricer, PriceStub


@scenario(
    "pricer.feature",
    "Pricing a basket with multiple items and offers.",
    example_converters=dict(
        apples=int,
        oranges=int,
        sub_total=float,
        discount=float,
        total=float,
    ),
)
def test_pricer() -> None:
    pass


@given(
    "I have a basket with <apples> apples and <oranges> oranges.",
    target_fixture="basket",
)
def set_basket(apples: int, oranges: int) -> Basket:
    return Basket(
        {
            "apple": apples,
            "orange": oranges,
        }
    )


@given("Apples cost 1.0 and oranges cost 2.0.", target_fixture="catalogue")
def set_catalogue() -> Catalogue:
    return Catalogue(
        {
            "apple": 1.0,
            "orange": 2.0,
        }
    )


@pytest.fixture
def offers() -> List[Offer]:
    return []


@when("Apples are buy one get one free.")
def apples_are_buy_one_get_one_free(
    offers: List[Offer], buy_one_apple_get_one_free: Offer
) -> None:
    offers.append(buy_one_apple_get_one_free)


@when("Oranges are half price.")
def oranges_are_half_price(offers: List[Offer], half_price_oranges: Offer) -> None:
    offers.append(half_price_oranges)


@then("The sub_total price should be <sub_total>.")
def check_sub_total(
    sub_total: float, basket: Basket, catalogue: Catalogue, offers: List[Offer]
) -> None:
    Pricer(basket, catalogue, offers).sub_total == sub_total


@then("A discount of <discount> should be applied.")
def check_discount(
    discount: float, basket: Basket, catalogue: Catalogue, offers: List[Offer]
) -> None:
    Pricer(basket, catalogue, offers).discount == discount


@then("The total price should be <total>.")
def check_total(
    total: float, basket: Basket, catalogue: Catalogue, offers: List[Offer]
) -> None:
    Pricer(basket, catalogue, offers).total == total
