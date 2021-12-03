# pylint: disable=C0103

from dataclasses import dataclass
from typing import Callable, List, TypeVar

from .stubs import PriceStub

T = TypeVar("T")
Transform = Callable[[T], T]


@dataclass
class Offer:
    title: str
    transform: Transform[List[PriceStub]]
