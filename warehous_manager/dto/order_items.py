from decimal import Decimal
from dataclasses import dataclass


@dataclass
class OrderItemsDTO:
    product_count: int
    product_price: Decimal
    product_name: str

    def __post_init__(self):
        self.product_price = float(self.product_price)


@dataclass
class MidDataItemsDTO:
    id: int
    price: Decimal#int
    name: str#int
