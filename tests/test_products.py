import pytest
from unittest.mock import AsyncMock
from decimal import Decimal

from warehous_manager.services.products import ProductService
from warehous_manager.repositories.products import ProductRepository
from warehous_manager.dto.products import (
    ProductUpdateDTO,
    ProductResponseDTO,
    ProductCreateDTO)



async def create_product(mocker):
    product_data = ProductCreateDTO(
        name='Test Name',
        description='descr',
        price=Decimal('100'),
        product_count=10
    )
    response = ProductResponseDTO(
        id=1,
        name='Test Name',
        description='descr',
        price=Decimal('100'),
        product_count=10
    )
    mock_repo = mocker.MagicMock(ProductRepository)
    mock_repo.add_one = AsyncMock(
        return_value=product_data
    )
    service = ProductService(product_repo=mock_repo)
    product = await service.create(data=product_data)
    return response


@pytest.mark.asyncio
async def test_create_product(mocker):
    product = await create_product(mocker)

    assert product.name == "Test Name"
    assert product.price == 100.0
    assert product.product_count == 10
    assert product.id == 1


@pytest.mark.asyncio
async def test_get_product(mocker):
    mock_product = await create_product(mocker)
    product_id = 1
    mock_repo = mocker.MagicMock(ProductRepository)
    mock_repo.get_one = AsyncMock(
        return_value=mock_product
    )
    service = ProductService(product_repo=mock_repo)
    product = await service.get(product_id=product_id)

    assert product.name == "Test Name"
    assert product.price == 100.0
    assert product.product_count == 10


@pytest.mark.asyncio
async def test_update_product(mocker):
    original_product = await create_product(mocker)
    update_data = {
        "name": "Updated Product Name"
    }
    mock_repo = mocker.MagicMock(ProductRepository)
    mock_repo.get_one = AsyncMock(
        return_value=original_product
    )

    updated_product = original_product
    updated_product.name = "Updated Product Name"

    mock_repo.update_one = AsyncMock(
        return_value=updated_product
    )
    service = ProductService(product_repo=mock_repo)
    updated_product = await service.update(
        product_id=1,
        data=updated_product
    )

    assert updated_product.name == "Updated Product Name"
    assert updated_product.price == 100.0
    assert updated_product.product_count == 10


@pytest.mark.asyncio
async def test_delete_product(mocker):
    mock_product = await create_product(mocker)
    product_id=1
    mock_repo = mocker.MagicMock(ProductRepository)
    mock_repo.get_one = AsyncMock(return_value=mock_product)
    service = ProductService(product_repo=mock_repo)
    message = await service.delete(product_id=product_id)

    assert message == f'product deleted'


@pytest.mark.asyncio
async def test_get_products(mocker):
    product1 = await create_product(mocker)
    mock_repo = mocker.MagicMock(ProductRepository)
    mock_repo.get_objects = AsyncMock(return_value=[product1])
    service = ProductService(product_repo=mock_repo)
    products = await service.get_all()

    assert len(products) == 1
    assert type(products) == list
    assert products[0].id == 1
