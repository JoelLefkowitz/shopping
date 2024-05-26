from ..utils.types import dict_matches_type
from .exceptions import CataloguePriceError, CatalogueTypeError, UnknownPrice
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Catalogue:
    products: Dict[str, float]

    def __init__(self, products: Optional[Dict[str, float]] = None) -> None:
        """
        Initialize a Catalogue instance.

        Args:
            products (Optional[Dict[str, float]], optional): Dictionary representing
            products and their prices. Defaults to None.

        Raises:
            CatalogueTypeError: Catalogue products must be a dictionary of strings to floats.
            CataloguePriceError: Catalogue products prices must be float values.
        """

        # We use None over {} as the default argument since it's immutable.
        if products is None:
            self.products = {}

        else:
            if not isinstance(products, dict) or not dict_matches_type(
                products, str, float
            ):
                raise CatalogueTypeError(products)

            for name, price in products.items():
                if price <= 0:
                    raise CataloguePriceError(name, products)

            self.products = products

    def __contains__(self, item: Any) -> bool:
        """
        Check if an item is in the catalogue.

        Args:
            item (Any): Item to check.

        Returns:
            bool: True if the item is in the catalogue.
        """
        return item in self.products

    @property
    def product_names(self) -> List[str]:
        """
        Get a list of the product names in a catalogue.

        Returns:
            List[str]: List of product names.
        """
        return list(self.products)

    def price(self, name: str) -> float:
        """
        Get the price of an item in a catalogue.

        Args:
            name (str): Item name.

        Raises:
            UnknownPrice: Product name is not in the catalogue.

        Returns:
            float: Price of the product.
        """
        if name not in self.products:
            raise UnknownPrice(name, self.product_names)

        return self.products[name]
