from dataclasses import asdict

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
from warehous_manager.dto.products import (
    ProductCreateDTO,
    ProductResponseDTO,
    ProductUpdateDTO
)


router = APIRouter(
    prefix='/products',
    tags=['Products']
)


@router.post(
    '/',
    response_model=ProductResponseDTO
)
async def create_product(product_data: ProductCreateSchema):
    try:
        product_data = ProductCreateDTO(
            **product_data.model_dump()
        )
        async with db_session() as s:
            repository = ProductRepository(s)
            product = await ProductService(
                product_repo=repository
            ).create(data=product_data)
        return JSONResponse(
            content=asdict(
                product,
                dict_factory=dict
            ),
            status_code=201
        )
    except ValidationError:
        return JSONResponse(
            content={'error': 'incorrect request data'},
            status_code=422
        )
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )


@router.get(
    '/',
    response_model=list
)
async def get_products():
    try:
        async with db_session() as s:
            repository = ProductRepository(s)
            products = await ProductService(
                product_repo=repository
            ).get_all()
            data = [
                asdict(
                    product,
                    dict_factory=dict
                ) for product in products
            ]
        return JSONResponse(
            content=data,
            status_code=200
        )
    except Exception:
        return JSONResponse(
            content={'error': 'server error'},
            status_code=500
        )


@router.get(
    '/{id}',
    response_model=ProductResponseDTO
)
async def get_product(id: int):
    try:
        async with db_session() as s:
            repository = ProductRepository(s)
            product = await ProductService(
                product_repo=repository
            ).get(product_id=id)
        return JSONResponse(
            content=asdict(product, dict_factory=dict),
            status_code=200
        )
    except ValidationError:
        return JSONResponse(
            content={'error': 'incorrect request data'},
            status_code=422
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




@router.put(
    '/{id}',
    response_model=ProductResponseDTO
)
async def update_product(
        id: int,
        update_data: ProductUpdateSchema):
    try:
        update_data = ProductUpdateDTO(
            **update_data.model_dump()
        )
        async with db_session() as s:
            repository = ProductRepository(s)
            product = await ProductService(
                product_repo=repository
            ).update(product_id=id, data=update_data)
        return JSONResponse(
            content=asdict(product, dict_factory=dict),
            status_code=201
        )
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


@router.delete(
    '/{id}',
    response_model=str
)
async def delete_product(id: int):
    try:
        async with db_session() as s:
            repository = ProductRepository(s)
            message = await ProductService(
                product_repo=repository
            ).delete(product_id=id)
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
