from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db.crud.base import CRUDBase
from app.core.db.models import Connection


class CRUDConnection(CRUDBase):
    async def get_connection_by_battery_id(
        self,
        battery_id: int,
        session: AsyncSession,
    ) -> Connection:
        """Получить соединение по id аккумулятора."""
        connection = await session.execute(
            select(Connection).where(
                Connection.battery_id == battery_id
            )
        )
        connection = connection.scalars().first()
        if connection is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=(f'Аккумулятора с id={battery_id} нет в базе'
                        ' или он не подключен ни к одному из устройств!')
            )
        return connection


connection_crud = CRUDConnection(Connection)
