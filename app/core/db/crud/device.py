from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select

from app.api.schemas.connection import ConnectionDB, ConnectionCreate
from app.core.db.crud.base import CRUDBase
from app.core.db.models import Device, Connection


class CRUDDevice(CRUDBase):
    async def create_connection(
        self,
        device_id: int,
        connection: ConnectionCreate,
        session: AsyncSession,
    ) -> ConnectionDB:
        """Получить все жалобы на объявление."""
        obj_in_data = connection.dict()
        connection = Connection(
            device_id=device_id,
            **obj_in_data,

        )
        session.add(connection)
        await session.commit()
        await session.refresh(connection)
        return connection


device_crud = CRUDDevice(Device)
