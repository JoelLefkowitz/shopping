from typing import Any, Dict


class ProductNotInBasket(Exception):
    def __init__(self, name: str, basket_contents: Dict[str, int]) -> None:
        super().__init__(
            f"""
            Product: '{name}' is not in the current basket.
            Basket contents: {basket_contents}
            """
        )


class BasketQuantityError(Exception):
    def __init__(self, name: str, basket_contents: Dict[str, int]) -> None:
        super().__init__(
            f"""
             Product quantities must be non-negative integers.
             Product: '{name}' is invalid.
             Basket contents: {basket_contents}
             """
        )


class BasketTypeError(Exception):
    def __init__(self, basket_contents: Any) -> None:
        super().__init__(
            f"""
             Basket contents must be a dictionary of strings to integers.
             Basket contents: {basket_contents}
             """
        )
