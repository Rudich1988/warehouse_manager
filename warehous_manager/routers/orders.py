from dataclasses import asdict

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic_core._pydantic_core import ValidationError
from sqlalchemy.exc import NoResultFound, IntegrityError

from warehous_manager.dto.orders import OrderResponseDTO, OrderCreateDTO
from warehous_manager.dto.products import ProductsItemsDTO
from warehous_manager.services.orders import OrderService
from warehous_manager.db.db import db_session
from warehous_manager.repositories.orders import OrderRepository
from warehous_manager.schemas.orders import (
    OrderCreateSchema,
    OrderUpdateStatusSchema
)


router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.get(
    '/',
    response_model=list
)
async def get_orders():
    try:
        async with db_session() as s:
            repository = OrderRepository(s)
            orders = await OrderService(
                order_repo=repository
            ).get_all()
            orders = [asdict(
                order,
                dict_factory=dict
            ) for order in orders
            ]
            return JSONResponse(
                content=orders,
                status_code=200
            )
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )


@router.post(
    '/',
    response_model=OrderResponseDTO
)
async def create_order(order_data: OrderCreateSchema):
    try:
        products = [
            ProductsItemsDTO(
                **product.model_dump()
            ) for product in order_data.products]
        order_data = OrderCreateDTO(
            products=products
        )
        async with db_session() as s:
            repository = OrderRepository(s)
            order = await OrderService(
                order_repo=repository
            ).create(data=order_data, session=s)
        return JSONResponse(
            content=asdict(order, dict_factory=dict),
            status_code=201
        )
    except NoResultFound:
        return JSONResponse(
            content={'error': 'product not found'},
            status_code=404
        )
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )
    

@router.get(
    '/{id}',
    response_model=OrderResponseDTO
)
async def get_order(id: int):
    try:
        async with db_session() as s:
            repository = OrderRepository(s)
            order = await OrderService(
                order_repo=repository
            ).get(order_id=id)
        return JSONResponse(
            content=asdict(order, dict_factory=dict),
            status_code=200
        )
    except NoResultFound:
        return JSONResponse(
            content={'error': 'order not found'},
            status_code=404
        )
    except IntegrityError:
        return JSONResponse(
            content={'error': 'incorrect request data'},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )


@router.patch(
    '/{id}/status',
    response_model=OrderResponseDTO
)
async def update_order_status(
        id: int,
        status: OrderUpdateStatusSchema
):
    try:
        async with db_session() as s:
            repository = OrderRepository(s)
            order_data = await OrderService(
                order_repo=repository
            ).update_order_status(
                status=status.model_dump()['status'],
                order_id=id
            )
            return JSONResponse(
                content=asdict(
                    order_data,
                    dict_factory=dict
                ),
                status_code=201
            )
    except ValidationError:
        return JSONResponse(
            content={'error': 'incorrect request data'},
            status_code=400
        )
    except NoResultFound:
        return JSONResponse(
            content={'error': 'order not found'},
            status_code=404
        )
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )
