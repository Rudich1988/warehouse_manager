from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic_core._pydantic_core import ValidationError
from sqlalchemy.exc import NoResultFound, IntegrityError

from warehous_manager.schemas.products import (
    ProductCreateSchema,
    ProductUpdateSchema
)
from warehous_manager.db.db import db_session
from warehous_manager.services.products import ProductService
from warehous_manager.repositories.products import ProductRepository


router = APIRouter(
    prefix='/products',
    tags=['Products']
)


@router.get('/')
async def get_products():
    try:
        async with db_session() as s:
            repository = ProductRepository(s)
            products = await ProductService(
                product_repo=repository
            ).get_all()
        return JSONResponse(content=products, status_code=200)
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )


@router.post('/')
async def create_product(request: Request):
    try:
        request = await request.json()
        product_data = ProductCreateSchema.model_validate(
            request
        ).model_dump()
        async with db_session() as s:
            repository = ProductRepository(s)
            product = await ProductService(
                product_repo=repository
            ).create(data=product_data)
        return JSONResponse(content=product, status_code=201)
    except ValidationError:
        return JSONResponse(
            content={'error': 'incorrect request data'},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )



@router.get('/{id}')
async def get_product(id: int):
    try:
        async with db_session() as s:
            repository = ProductRepository(s)
            product = await ProductService(
                product_repo=repository
            ).get(data={'id': id})
        return JSONResponse(content=product, status_code=200)
    except NoResultFound:
        return JSONResponse(
            content={'error': 'product not found'},
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



@router.put('/{id}')
async def update_product(id: int, request: Request):
    try:
        request = await request.json()
        product_data = ProductUpdateSchema.model_validate(
            request
        ).model_dump()
        async with db_session() as s:
            repository = ProductRepository(s)
            product = await ProductService(
                product_repo=repository
            ).update(product_id=id, data=product_data)
        return JSONResponse(content=product, status_code=201)
    except ValidationError:
        return JSONResponse(
            content={'error': 'incorrect request data'},
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



@router.delete('/{id}')
async def delete_product(id: int):
    try:
        async with db_session() as s:
            repository = ProductRepository(s)
            message = await ProductService(
                product_repo=repository
            ).delete(id=id)
        return JSONResponse(
            content={'success': message},
            status_code=200
        )
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
