# pylint: disable=E0401,W0611,W0621,R0913
import pytest
from fixtures.offers import buy_one_apple_get_one_free, half_price_oranges

from basket import Basket
from catalogue import Catalogue, UnknownPrice
from pricer import Offer, Pricer, PriceStub


def test_create(half_price_oranges: Offer) -> None:
    """
    Test that Prices instances can be initialized.
    """
    Pricer(Basket(), Catalogue())
    Pricer(Basket(), Catalogue(), [])
    Pricer(Basket(), Catalogue(), [])
    Pricer(Basket(), Catalogue(), [half_price_oranges])


def test_unknown_price_error() -> None:
    """
    Test that having an item in the basket who's price is not in the catalogue raises UnknownPrice.
    """
    with pytest.raises(UnknownPrice):
        Pricer(Basket({"a": 1}), Catalogue())


def test_stubs_list() -> None:
    """
    Test that the stubs list is a list of price stubs.
    """
    assert Pricer(Basket({"a": 1}), Catalogue({"a": 1.0})).stubs_list == [
        PriceStub("a", 1.0)
    ]


# We need to start injecting the dependencies as fixtures now to decouple these larger tests.
@pytest.mark.parametrize(
    "basket, catalogue, sub_total",
    [
        [Basket({}), Catalogue({}), 0.0],
        [Basket({"a": 1}), Catalogue({"a": 1.0}), 1.0],
        [Basket({"a": 2}), Catalogue({"a": 1.0}), 2.0],
        [Basket({"a": 1, "b": 1}), Catalogue({"a": 1.0, "b": 2.0}), 3.0],
    ],
)
def test_sub_total(basket: Basket, catalogue: Catalogue, sub_total: float) -> None:
    """
    Test that the sub total is the sum of the product non-discounted prices.

    Args:
        basket (Basket): A basket of items.
        catalogue (Catalogue): A catalogue of prices.
        sub_total (float): The expected sub_total.
    """
    assert Pricer(basket, catalogue).sub_total == sub_total


# This test covers both the discount and total properties.
# It is appropriate to merge them since they are coupled properties.
@pytest.mark.parametrize(
    "basket, sub_total, discount, total",
    [
        [Basket(), 0.0, 0.0, 0.0],
        [Basket({"apple": 1}), 1.0, 0.0, 1.0],
        [Basket({"apple": 2}), 2.0, 1.0, 1.0],
        [Basket({"apple": 3}), 3.0, 1.0, 2.0],
        [Basket({"orange": 1}), 2.0, 1.0, 1.0],
        [Basket({"orange": 2}), 4.0, 2.0, 2.0],
        [Basket({"apple": 1, "orange": 1}), 3.0, 1.0, 2.0],
        [Basket({"apple": 2, "orange": 2}), 6.0, 3.0, 3.0],
    ],
)
def test_offers(
    basket: Basket,
    sub_total: float,
    discount: float,
    total: float,
    buy_one_apple_get_one_free: Offer,
    half_price_oranges: Offer,
) -> None:
    """
    Tests that total, sub_total and discount are the calculated based on the final price
    of the basket products after applying all offers.

    Args:
        basket (Basket): A basket of items.
        sub_total (float): The expected sub_total.
        discount (float): The expected discount.
        total (float): The expected total.
        buy_one_apple_get_one_free (Offer): Buy one apple get one free offer.
        half_price_oranges (Offer): Half price oranges offer.
    """
    pricer = Pricer(
        basket,
        Catalogue({"apple": 1.0, "orange": 2.0}),
        [buy_one_apple_get_one_free, half_price_oranges],
    )

    assert pricer.sub_total == sub_total
    assert pricer.discount == discount
    assert pricer.total == total
