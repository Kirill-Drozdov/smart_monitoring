from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.schemas.battery import BatteryDB
from app.core.db.crud.base import CRUDBase
from app.core.db.models import Device, Connection, Battery


class CRUDDevice(CRUDBase):
    async def get_connected_batteries(
        self,
        device_id: int,
        session: AsyncSession,
    ) -> list[BatteryDB]:
        """Получить все подключенные аккумуляторы."""
        battery_ids = await session.execute(
            select(Connection.battery_id).where(
                Connection.device_id == device_id
            )
        )
        battery_ids = battery_ids.scalars().all()
        if not battery_ids:
            raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='К этому устройству не подключен ни один аккумулятор!',
        )
        batteries = await session.execute(
            select(Battery).where(
                Battery.id.in_(battery_ids)
            )
        )
        batteries = batteries.scalars().all()
        return batteries


device_crud = CRUDDevice(Device)
