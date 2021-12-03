from typing import Any, Dict

import pytest

from catalogue import (Catalogue, CataloguePriceError, CatalogueTypeError,
                       UnknownPrice)


def test_create() -> None:
    """
    Test that Catalogue instances can be initialized.
    """
    Catalogue()
    Catalogue({})
    Catalogue({"a": 1.0})


@pytest.mark.parametrize(
    "products",
    [{"a": "1.0"}, {1: "a"}, {"a": 1}],
)
def test_catalogie_type_error(products: Any) -> None:
    """
    Test that initializing a Catalogue with products that
    have an invalid type raises a CatalogueTypeError.

    Args:
        products (Any): Products that have an invalid type.
    """
    with pytest.raises(CatalogueTypeError):
        Catalogue(products)  # type: ignore


@pytest.mark.parametrize(
    "products",
    [
        {"a": 0.0},
        {"a": -1.0},
    ],
)
def test_catalogie_price_error(products: Dict[str, float]) -> None:
    """
    Test that initializing a Catalogue with products that
    have an invalid price raises a CataloguePriceError.

    Args:
        contents (Any): Products that have an invalid price.
    """
    with pytest.raises(CataloguePriceError):
        Catalogue(products)  # type: ignore


def test_contains() -> None:
    """
    Tests that products in the catalogue return True to
    the right handside of the 'in' operator.
    """
    assert "a" in Catalogue({"a": 1.0})
    assert "b" not in Catalogue({"a": 1.0})


def test_product_names() -> None:
    """
    Tests that catalogue's product names is a list of the
    names of the products in the catalogue.
    """
    assert Catalogue({"a": 1.0, "b": 1.0}).product_names == ["a", "b"]


def test_price() -> None:
    """
    Tests that the price of an item returns
    the price of that item in the catalogue.
    """
    assert Catalogue({"a": 1.0, "b": 1.0}).price("a") == 1.0


def test_unknown_price_error() -> None:
    """
    Test that getting the price of an item not in the catalogue raises UnknownPrice.
    """
    with pytest.raises(UnknownPrice):
        Catalogue({"a": 1.0}).price("b")
