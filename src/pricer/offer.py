from .stubs import PriceStub
from dataclasses import dataclass
from typing import Callable, List, TypeVar

T = TypeVar("T")
Transform = Callable[[T], T]


@dataclass
class Offer:
    title: str
    transform: Transform[List[PriceStub]]
