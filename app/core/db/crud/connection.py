from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db.crud.base import CRUDBase
from app.core.db.crud.battery import battery_crud
from app.core.db.crud.device import device_crud
from app.core.db.models import Connection


class CRUDConnection(CRUDBase):
    async def get_connection_by_battery_id(
        self,
        battery_id: int,
        session: AsyncSession,
    ) -> Connection:
        """Получить соединение по id аккумулятора."""
        await battery_crud.is_exist(battery_id, session)
        connection = await session.execute(
            select(Connection).where(
                Connection.battery_id == battery_id
            )
        )
        connection = connection.scalars().first()
        if connection is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=(
                    f'Аккумулятор с id={battery_id} не'
                    ' подключен ни к одному из устройств!')
            )
        return connection

    async def get_connections_by_device_id(
        self,
        device_id: int,
        session: AsyncSession,
    ) -> Connection:
        """Получить соединения по id устройства."""
        await device_crud.is_exist(device_id, session)
        connections = await session.execute(
            select(Connection).where(
                Connection.device_id == device_id
            )
        )
        connections = connections.scalars().all()
        if not connections:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=(f'К устройству с id={device_id} не подключен'
                        ' ни один аккумулятор!')
            )
        return connections


connection_crud = CRUDConnection(Connection)
