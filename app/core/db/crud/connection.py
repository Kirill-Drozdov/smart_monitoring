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
        return connection.scalars().first()


connection_crud = CRUDConnection(Connection)
