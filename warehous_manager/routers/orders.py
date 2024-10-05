import json

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic_core._pydantic_core import ValidationError


from warehous_manager.services.orders import OrderService
from warehous_manager.db.db import db_session
from warehous_manager.repositories.orders import OrderRepository
from warehous_manager.schemas.orders import OrderCreateSchema, OrderUpdateSchema


router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.get('/')
async def get_orders():
    pass


@router.post('/')
async def create_order(request: Request):
    #try
    request = await request.json()
    order_data = OrderCreateSchema.model_validate(
        request
    ).model_dump()
    async with db_session() as s:
        repository = OrderRepository(s)
        order = await OrderService(
            order_repo=repository
        ).create(data=order_data, session=s)
    return JSONResponse(content=order, status_code=201)
    # except ValidationError:
    #   return return JSONResponse(content={'error': 'некорректные данные запроса'}, status_code=400)


@router.get('/{id}')
async def get_order(id: int):
    #try
    async with db_session() as s:
        repository = OrderRepository(s)
        order = await OrderService(
            order_repo=repository
        ).get(data={'id': id})
    return JSONResponse(content=order, status_code=200)
    # except NoResultFound:
    #   return JSONResponse(content={'error': 'order not found'}, status_code=400)
    # except IntegrityError:
    #   return return JSONResponse(content={'error': 'incorrect request data'}, status_code=400)


@router.patch('/{id}/status')
async def update_order_status(id: int, request: Request):
    #try:
    request = await request.json()
    order_data = OrderUpdateSchema.model_validate(
        request
    ).model_dump()
    async with db_session() as s:
        repository = OrderRepository(s)
        order_data = OrderService
