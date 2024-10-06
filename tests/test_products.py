import pytest
from unittest.mock import AsyncMock
from decimal import Decimal

from warehous_manager.services.products import ProductService
from warehous_manager.repositories.products import ProductRepository
from warehous_manager.schemas.products import ProductResponseSchema


async def create_product(mocker, id: int):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": Decimal('100'),
        "quantity": 10
    }
    mock_product = ProductResponseSchema(
        id=id,
        **product_data
    )
    mock_repo = mocker.MagicMock(ProductRepository)
    mock_repo.add_one = AsyncMock(
        return_value=mock_product
    )
    service = ProductService(product_repo=mock_repo)
    product = await service.create(data=product_data)
    return product


@pytest.mark.asyncio
async def test_create_product(mocker):
    product = await create_product(mocker, id=1)

    assert product["name"] == "Test Product"
    assert product["price"] == 100.0
    assert product["quantity"] == 10


@pytest.mark.asyncio
async def test_get_product(mocker):
    mock_product = await create_product(mocker, id=1)
    data = {'id': 1}
    mock_repo = mocker.MagicMock(ProductRepository)
    mock_repo.get_one = AsyncMock(
        return_value=mock_product
    )
    service = ProductService(product_repo=mock_repo)
    product = await service.get(data=data)

    assert product["name"] == "Test Product"
    assert product["price"] == 100.0
    assert product["quantity"] == 10


@pytest.mark.asyncio
async def test_update_product(mocker):
    original_product = await create_product(mocker, id=1)
    update_data = {
        "name": "Updated Product Name"
    }
    mock_repo = mocker.MagicMock(ProductRepository)
    mock_repo.get_one = AsyncMock(
        return_value=original_product
    )

    updated_product = original_product
    updated_product["name"] = "Updated Product Name"

    mock_repo.update_one = AsyncMock(
        return_value=updated_product
    )
    service = ProductService(product_repo=mock_repo)
    updated_product = await service.update(
        product_id=1,
        data=update_data
    )

    assert updated_product["name"] == "Updated Product Name"
    assert updated_product["price"] == 100.0
    assert updated_product["quantity"] == 10


@pytest.mark.asyncio
async def test_delete_product(mocker):
    mock_product = await create_product(mocker, id=1)
    product_id=1
    mock_repo = mocker.MagicMock(ProductRepository)
    mock_repo.get_one = AsyncMock(return_value=mock_product)
    service = ProductService(product_repo=mock_repo)
    message = await service.delete(id=product_id)

    assert message == f'product id: {product_id} deleted'


@pytest.mark.asyncio
async def test_get_products(mocker):
    product1 = await create_product(mocker, id=1)
    product2 = await create_product(mocker, id=2)
    mock_repo = mocker.MagicMock(ProductRepository)
    mock_repo.get_objects = AsyncMock(return_value=[product1, product2])
    service = ProductService(product_repo=mock_repo)
    products = await service.get_all()

    assert len(products) == 2
    assert products[0]['id'] == 1
    assert products[1]['id'] == 2
