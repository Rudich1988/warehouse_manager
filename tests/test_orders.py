import pytest
from unittest.mock import AsyncMock
from decimal import Decimal
from warehous_manager.services.orders import OrderService
from warehous_manager.repositories.orders import OrderRepository
from warehous_manager.dto.orders import OrderResponseDTO
from warehous_manager.dto.order_items import OrderItemsDTO
from datetime import datetime
from warehous_manager.enams.statuses import Statuses


@pytest.mark.asyncio
async def test_get_order(mocker):
    order_response_data = OrderResponseDTO(
        id=1,
        created_at=datetime.now(),
        status=Statuses.IN_PROGRESS,
        items=[
            OrderItemsDTO(
                product_count=2,
                product_name="Product 1",
                product_price=Decimal("100.00")
            )
        ],
        product_count=2,
        order_cost=Decimal("200.00")
    )

    mock_order_repo = mocker.MagicMock(OrderRepository)
    mock_order_repo.get_one = AsyncMock(
        return_value=order_response_data
    )

    order_service = OrderService(
        order_repo=mock_order_repo
    )

    result = await order_service.get(order_id=1)

    assert result.id == 1
    assert result.product_count == 2
    assert result.order_cost == 200.00
    assert len(result.items) == 1
    assert result.items[0].product_name == "Product 1"


@pytest.mark.asyncio
async def test_get_orders(mocker):
    order_1 = OrderResponseDTO(
        id=1,
        created_at=datetime.now(),
        status=Statuses.IN_PROGRESS,
        items=[
            OrderItemsDTO(
                product_count=2,
                product_name="Product 1",
                product_price=Decimal("100.00")
            )
        ],
        product_count=2,
        order_cost=Decimal("200.00")
    )
    order_2 = OrderResponseDTO(
        id=2,
        created_at=datetime.now(),
        status=Statuses.IN_PROGRESS,
        items=[
            OrderItemsDTO(
                product_count=10,
                product_name="Product 2",
                product_price=Decimal("235.00")
            )
        ],
        product_count=10,
        order_cost=Decimal("2350.00")
    )
    orders = [order_1, order_2]
    mock_order_repo = mocker.MagicMock(OrderRepository)
    mock_order_repo.get_objects = AsyncMock(return_value=orders)
    order_service = OrderService(
        order_repo=mock_order_repo
    )

    result = await order_service.get_all()

    assert len(result) == 2
    assert type(result) == list
    assert result[0].id == 1
    assert result[1].id == 2
    assert result[1].order_cost == Decimal('2350.00')


@pytest.mark.asyncio
async def test_update_order_status(mocker):
    original_order = OrderResponseDTO(
        id=1,
        created_at=datetime.now(),
        status=Statuses.IN_PROGRESS,
        items=[
            OrderItemsDTO(
                product_count=2,
                product_name="Product 1",
                product_price=Decimal("100.00")
            )
        ],
        product_count=2,
        order_cost=Decimal("200.00")
    )

    updated_order = original_order
    updated_order.status = Statuses.SENT

    mock_order_repo = mocker.MagicMock(
        OrderRepository
    )
    mock_order_repo.update_status = AsyncMock(
        return_value=updated_order
    )

    order_service = OrderService(
        order_repo=mock_order_repo
    )

    result = await order_service.update_order_status(
        order_id=1,
        status=Statuses.SENT
    )

    assert result.status == Statuses.SENT
    assert result.id == 1
    assert result.order_cost == 200.00
