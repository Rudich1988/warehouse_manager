from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic_core._pydantic_core import ValidationError
from sqlalchemy.exc import NoResultFound, IntegrityError


from warehous_manager.services.orders import OrderService
from warehous_manager.db.db import db_session
from warehous_manager.repositories.orders import OrderRepository
from warehous_manager.schemas.orders import OrderCreateSchema, OrderUpdateStatusSchema


router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.get('/')
async def get_orders():
    try:
        async with db_session() as s:
            repository = OrderRepository(s)
            orders = await OrderService(
                order_repo=repository
            ).get_all()
            return JSONResponse(
                content=orders,
                status_code=200
            )
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )


@router.post('/')
async def create_order(request: Request):
    try:
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
    except NoResultFound:
        return JSONResponse(
            content={'error': 'product not found'},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )


@router.get('/{id}')
async def get_order(id: int):
    try:
        async with db_session() as s:
            repository = OrderRepository(s)
            order = await OrderService(
                order_repo=repository
            ).get(data={'id': id})
        return JSONResponse(
            content=order,
            status_code=200
        )
    except NoResultFound:
        return JSONResponse(
            content={'error': 'order not found'},
            status_code=400
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


@router.patch('/{id}/status')
async def update_order_status(id: int, request: Request):
    try:
        request = await request.json()
        order_data = OrderUpdateStatusSchema.model_validate(
            request
        ).model_dump()
        async with db_session() as s:
            repository = OrderRepository(s)
            order_data = await OrderService(
                order_repo=repository
            ).update_order_status(
                status=order_data['status'],
                order_id=id
            )
            return JSONResponse(
                content=order_data,
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
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )

