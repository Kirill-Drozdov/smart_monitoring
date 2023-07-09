from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models import User, Connection

BATTERIES_LIMIT = 5


async def check_battery_is_not_already_connected(
        connection: Connection,
        session: AsyncSession,
) -> None:
    """Проверяет, что аккумулятор не подключен к другим устройствам."""
    exists_criteria = (
        select(Connection).where(
            Connection.battery_id == connection.battery_id
        ).exists()
    )
    db_connection_exists = await session.execute(
        select(True).where(
            exists_criteria
        )
    )
    db_connection_exists = db_connection_exists.scalars().first()
    if db_connection_exists:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=(
                f'Аккумулятор с id={connection.battery_id} '
                f'уже подключен к устройству с id={connection.device_id}!'
            ),
        )


async def check_batteries_limit(
        device_id: int,
        session: AsyncSession,
) -> None:
    """Проверяет, что не превышен лимит подключенных аккумуляторов."""
    count_connected_batteries = await session.execute(
        select(func.count(Connection.device_id)).where(
            Connection.device_id == device_id
        )
    )
    if count_connected_batteries.scalars().first() >= BATTERIES_LIMIT:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=('Вы не можете подключать к одному '
                    f'устройству более {BATTERIES_LIMIT} аккумуляторов.')
        )


async def check_user_update_delete_rights(
        obj_db,
        user: User,
) -> None:
    """Проверка прав пользователя на редактирование/удаление записи."""
    if obj_db.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='У Вас нет прав на осуществление данного действия!'
        )
    return obj_db


async def check_user_create_rights(
        obj_db,
        user: User,
) -> None:
    """Проверка прав пользователя на создание записи."""
    if obj_db.user_id == user.id and not user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='У Вас нет прав на осуществление данного действия!'
        )
    return obj_db
