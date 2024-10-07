from typing import Literal, List
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal

from warehous_manager.enams.statuses import Statuses
from warehous_manager.dto.order_items import OrderItemsDTO
from warehous_manager.dto.products import ProductsItemsDTO


@dataclass
class OrderCreateDTO:
    products: List[ProductsItemsDTO]


class OrderUpdateStatusDTO:
    status: Literal[
    Statuses.IN_PROGRESS,
    Statuses.SENT,
    Statuses.DELIVERED
    ]

@dataclass
class OrderResponseDTO:
    id: int
    created_at: datetime
    status: Literal[
        Statuses.IN_PROGRESS,
        Statuses.SENT,
        Statuses.DELIVERED
    ]
    items: list[OrderItemsDTO]
    order_cost: Decimal
    product_count: int

    def __post_init__(self):
        self.order_cost = float(self.order_cost)
        self.created_at = str(self.created_at)
