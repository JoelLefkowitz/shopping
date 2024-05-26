import pytest
from src.basket.basket import Basket
from src.basket.exceptions import (BasketQuantityError, BasketTypeError,
                                   ProductNotInBasket)
from typing import Any, Dict


def test_create() -> None:
    """
    Test that Basket instances can be initialized.
    """
    Basket()
    Basket({})
    Basket({"a": 1})


@pytest.mark.parametrize(
    "contents",
    [{"a": "1"}, {1: "a"}, {"a": 1.0}],
)
def test_basket_type_error(contents: Any) -> None:
    """
    Test that initializing a Basket with contents that
    have an invalid type raises a BasketTypeError.

    Args:
        contents (Any): Contents that have an invalid type.
    """
    with pytest.raises(BasketTypeError):
        Basket(contents)  # type: ignore


@pytest.mark.parametrize(
    "contents",
    [{"a": 0}, {"a": -1}],
)
def test_basket_quantity_error(contents: Dict[str, int]) -> None:
    """
    Test that initializing a Basket with contents that
    have invalid quantities raises a BasketQuantityError.

    Args:
        contents ([type]): Contents that have invalid quantities.
    """
    with pytest.raises(BasketQuantityError):
        Basket(contents)  # type: ignore


def test_contains() -> None:
    """
    Tests that products in the basket return True to
    the right handside of the 'in' operator.
    """
    assert "a" in Basket({"a": 1})
    assert "b" not in Basket({"a": 1})


@pytest.mark.parametrize(
    "contents, count",
    [
        [{}, 0],
        [{"a": 1}, 1],
        [{"a": 2}, 2],
        [{"a": 1, "b": 1}, 2],
    ],
)
def test_count(contents: Dict[str, int], count: int) -> None:
    """
    Tests that the basket count is the sum of the quantities in the basket.

    Args:
        contents (Dict[str, int]): Basket contents.
        count (int): Expected count.
    """
    assert Basket(contents).count == count


def test_quantity() -> None:
    """
    Tests that the quantity of an item is its quantity in the basket.
    """
    assert Basket().quantity("a") == 0
    assert Basket({"a": 1}).quantity("a") == 1


@pytest.mark.parametrize(
    "contents, item, result",
    [
        [{}, "a", {"a": 1}],
        [{"a": 1}, "a", {"a": 2}],
        [{"a": 1}, "b", {"a": 1, "b": 1}],
    ],
)
def test_add(contents: Dict[str, int], item: str, result: Dict[str, int]) -> None:
    """
    Tests that you can add items to the basket.

    Args:
        contents (Dict[str, int]): Starting basket contents.
        item (str): Product to add to the basket.
        result (Dict[str, int]): Expected basket after adding the product.
    """
    basket = Basket(contents)
    basket.add(item)
    assert basket.contents == result


@pytest.mark.parametrize(
    "contents, item, result",
    [
        [{"a": 1}, "a", {}],
        [{"a": 2}, "a", {"a": 1}],
    ],
)
def test_remove(contents: Dict[str, int], item: str, result: Dict[str, int]) -> None:
    """
    Tests that you can remove items from the basket.

    Args:
        contents (Dict[str, int]): Starting basket contents.
        item (str): Product to remove from the basket.
        result (Dict[str, int]): Expected basket after removing the product.
    """
    basket = Basket(contents)
    basket.remove(item)
    assert basket.contents == result


def test_product_not_in_basket_error() -> None:
    """
    Tests that removing an item not in the basket raises a ProductNotInBasket.
    """
    with pytest.raises(ProductNotInBasket):
        Basket().remove("a")
