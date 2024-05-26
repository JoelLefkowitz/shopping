import pytest
from src.pricer.offer import Offer
from src.pricer.pricer import PriceStub
from typing import List


def buy_one_apple_get_one_free_transform(
    stubs_list: List[PriceStub],
) -> List[PriceStub]:
    apples = [i for i, x in enumerate(stubs_list) if x.name == "apple"]
    return [
        PriceStub("apple", 0.0) if i in apples[1::2] else x
        for i, x in enumerate(stubs_list)
    ]


def half_price_oranges_transform(stubs_list: List[PriceStub]) -> List[PriceStub]:
    return [
        PriceStub(i.name, i.price / 2 if i.name == "orange" else i.price)
        for i in stubs_list
    ]


@pytest.fixture()
def buy_one_apple_get_one_free() -> Offer:
    return Offer("Buy one apple get one free", buy_one_apple_get_one_free_transform)


@pytest.fixture()
def half_price_oranges() -> Offer:
    return Offer("Half price oranges", half_price_oranges_transform)
