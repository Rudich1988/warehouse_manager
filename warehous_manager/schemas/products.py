from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class ProductCreateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(min_length=3)
    description: str = Field(min_length=3)
    price: Decimal = Field(ge=0)
    quantity: int = Field(ge=0)


class ProductUpdateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=3)
    price: Optional[float] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)


class ProductResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: float
    quantity: int
