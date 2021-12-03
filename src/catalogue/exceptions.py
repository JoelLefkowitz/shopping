from typing import Any, Dict, List


class CatalogueTypeError(Exception):
    def __init__(self, catalogue_products: Any) -> None:
        super().__init__(
            f"""
             Catalogue products must be a dictionary of strings to floats.
             Products: {catalogue_products}
             """
        )


class CataloguePriceError(Exception):
    def __init__(self, name: str, catalogue_products: Dict[str, float]) -> None:
        super().__init__(
            f"""
             Catalogue products prices must be float values.
             Product: '{name}' is invalid.
             Products: {catalogue_products}
             """
        )


class UnknownPrice(Exception):
    def __init__(self, name: str, catalogue_names: List[str]) -> None:
        super().__init__(
            f"""
             Product: '{name}' is not in the catalogue.
             Catalogue product names: {catalogue_names}
             """
        )
