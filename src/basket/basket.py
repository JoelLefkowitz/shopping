from ..utils.types import dict_matches_type
from .exceptions import (BasketQuantityError, BasketTypeError,
                         ProductNotInBasket)
from dataclasses import dataclass
from typing import Any, Dict, ItemsView, Iterator, Optional


@dataclass
class Basket:
    contents: Dict[str, int]

    def __init__(self, contents: Optional[Dict[str, int]] = None) -> None:
        """
        Initialize a Basket instance.

        Args:
            contents (Optional[Dict[str, int]], optional): Dictionary representing
            products and their quantities in the basket. Defaults to None.

        Raises:
            BasketTypeError: Basket contents must be a dictionary of strings to integers.
            BasketQuantityError: Product quantities must be non-negative integers.
        """

        # We use None over {} as the default argument since it's immutable.
        if contents is None:
            self.contents = {}

        else:
            if not isinstance(contents, dict) or not dict_matches_type(
                contents, str, int
            ):
                raise BasketTypeError(contents)

            for name, quantity in contents.items():
                if quantity <= 0:
                    raise BasketQuantityError(name, contents)

            self.contents = contents

    def __contains__(self, item: Any) -> bool:
        """
        Check if an item is in the basket contents.

        Args:
            item (Any): Item to check.

        Returns:
            bool: True if the item is in the basket contents.
        """
        return item in self.contents

    def __iter__(self) -> Iterator[str]:
        """
        Iterate through a basket.

        Yields:
            Iterator[str]: Basket contents iterator.
        """
        return iter(self.contents)

    @property
    def count(self) -> int:
        """
        Get the total number of items in the basket.

        Returns:
            int: The number of items in the basket.
        """
        return sum(self.contents.values())

    def items(self) -> ItemsView[str, int]:
        """
        Iterate through a basket's key value pairs.

        Returns:
            ItemsView[str, int]: Zipped dictionary items.
        """
        return self.contents.items()

    def quantity(self, name: str) -> int:
        """
        Get the quantity of a product in the basket.

        Args:
            name (str): Product name.

        Returns:
            int: The quantity of the product in the basket.
        """
        return self.contents[name] if name in self.contents else 0

    def add(self, name: str) -> None:
        """
        Add an item to the basket.

        Args:
            name (str): Product name.
        """
        if name in self.contents:
            self.contents[name] += 1
        else:
            self.contents[name] = 1

    def remove(self, name: str) -> None:
        """
        Remove an item from the basket.

        Args:
            name (str): Product name.

        Raises:
            ProductNotInBasket: Product is not in the current basket.
        """
        if name not in self.contents:
            raise ProductNotInBasket(name, self.contents)

        self.contents[name] -= 1

        if self.contents[name] == 0:
            self.contents.pop(name)
