from http import HTTPStatus

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import Base
from app.core.db.models import User


class CRUDBase:
    """Базовый класс для типовых операций CRUD."""

    def __init__(self, model: Base):
        self.model = model

    async def is_exist(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """
        Проверяет, существует ли объект в БД.
        Если объект не найден, бросает ошибку.
        """
        exists_criteria = (
            select(self.model).where(
                self.model.id == obj_id
            ).exists()
        )
        db_obj_exists = await session.execute(
            select(True).where(
                exists_criteria
            )
        )
        db_obj_exists = db_obj_exists.scalars().first()
        if not db_obj_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Объект {self.model.__tablename__.title()} не найден!'
            )

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """
        Возвращает объект по id.
        """
        await self.is_exist(obj_id, session)
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Возвращает все объекты из БД."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            user: User,
            session: AsyncSession,
    ):
        """Создаёт объект в БД."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        """Обновляет объект в БД."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        """Удаляет объект из БД."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
