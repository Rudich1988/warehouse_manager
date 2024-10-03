from abc import ABC, abstractmethod

from sqlalchemy import delete, select
from sqlalchemy.exc import NoResultFound

from warehous_manager.db.db import Session


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, session: Session):
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, id):
        raise NotImplementedError

    @abstractmethod
    async def get_objects(self):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: Session):
        self.session = session

    async def add_one(self, data: dict):
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_one(self, data: dict):
        obj = await self.session.execute(
            select(self.model).filter_by(**data)
        )
        return obj.scalars().one()

    async def get_objects(self):
        products = await self.session.execute(
            select(self.model))
        return products.scalars().all()

    async def update_one(self, product_id: int, data: dict):
        obj = await self.get_one({'id': product_id})
        for key, value in data.items():
            if value is not None:
                setattr(obj, key, value)
        await self.session.flush()
        return obj

    async def delete_one(self, data: dict) -> int:
        obj = await self.get_one(data)
        await self.session.delete(obj)
        await self.session.flush()
