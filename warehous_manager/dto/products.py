from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class ProductCreateDTO:
    name: str
    description: str
    price: Decimal
    product_count: int


@dataclass
class ProductResponseDTO:
    id: int
    name: str
    description: str
    price: Decimal
    product_count: int

    def __post_init__(self):
        self.price = float(self.price)


@dataclass
class ProductUpdateDTO:
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    product_count: Optional[int]


@dataclass
class ProductsItemsDTO:
    id: int
    product_count: int
