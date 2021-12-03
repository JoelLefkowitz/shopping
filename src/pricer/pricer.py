from dataclasses import dataclass
from functools import reduce
from typing import List, Optional

from basket import Basket
from catalogue import Catalogue, UnknownPrice

from .offer import Offer
from .stubs import PriceStub


@dataclass
class Pricer:
    basket: Basket
    catalogue: Catalogue
    offers: List[Offer]

    def __init__(
        self, basket: Basket, catalogue: Catalogue, offers: Optional[List[Offer]] = None
    ) -> None:
        """
        Initialize a Pricer instance.

        Args:
            basket (Basket): A basket of items and their quantities.
            catalogue (Catalogue): A catalogue of items and their prices.
            offers (Optional[List[Offer]], optional): A list of offers to modify that
            modify the final prices of items in the basket. Defaults to None.

        Raises:
            UnknownPrice: A product in the basket is not listed in the catalogue.
        """
        for product in basket:
            if product not in catalogue:
                raise UnknownPrice(product, catalogue.product_names)

        self.basket = basket
        self.catalogue = catalogue

        # We use None over [] as the default argument since it's immutable.
        if offers is None:
            self.offers = []
        else:
            self.offers = offers

    @property
    def stubs_list(self) -> List[PriceStub]:
        """
        Converts the basket into a list of price stubs consisting
        of products and their current prices.

        Returns:
            List[PriceStub]: List of price stubs.
        """
        return [
            stub
            for name, quantity in self.basket.items()
            for stub in [PriceStub(name, self.catalogue.price(name))] * quantity
        ]

    @property
    def sub_total(self) -> float:
        """
        Get the value of all the items in the basket without offer applied.

        Returns:
            float: Sub-total value.
        """
        return sum(stub.price for stub in self.stubs_list)

    @property
    def discount(self) -> float:
        """
        Get the basket total amount discounted after applying offers.

        Returns:
            float: Total amount discounted
        """
        return self.sub_total - self.total

    @property
    def total(self) -> float:
        """
        Get the basket total cost after applying offers.

        Returns:
            float: Total cost.
        """

        # We fold through the offers here rather than using a for loop to invert
        # the control over the stub list's state.
        # We must use max(stub.price, 0) to drop negative price values to zero.
        return sum(
            [
                max(stub.price, 0)
                for stub in reduce(
                    lambda stubs_list, offer: offer.transform(stubs_list),  # type: ignore
                    self.offers,
                    self.stubs_list,
                )
            ]
        )
