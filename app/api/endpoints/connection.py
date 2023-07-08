from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_async_session
from app.core.user import current_user
from app.core.db.crud.connection import connection_crud
from app.core.db.models import User
from app.api.schemas.connection import (
    ConnectionCreate,
    ConnectionDB,
)
# from app.core.validators import (
#     check_user_update_delete_rights,
# )


connection_router = APIRouter()


@connection_router.post(
    '/',
    response_model=ConnectionDB,
    status_code=HTTPStatus.CREATED,
    summary="Установить соединение",
    response_description="Информация о созданном соединении",
)
async def create_new_connection(
        connection: ConnectionCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Установить соединение.

    - **device_id**: внешний ключ устройства
    - **battery_id**: внешний ключ аккумулятора
    """
    return await connection_crud.create(connection, user, session)


@connection_router.get(
    '/',
    response_model=list[ConnectionDB],
    status_code=HTTPStatus.OK,
    summary="Смотреть все соединения",
    response_description="Список всех соединений",
)
async def get_all_connections(
        session: AsyncSession = Depends(get_async_session),
):
    """Смотреть все соединения.

    - **device_id**: внешний ключ устройства
    - **battery_id**: внешний ключ аккумулятора
    - **id**: уникальный идентификатор соединения
    - **user_id**: внешний ключ пользователя, установившего соединение
    """
    return await connection_crud.get_multi(session)


@connection_router.delete(
    '/{connection_id}',
    response_model=ConnectionDB,
    status_code=HTTPStatus.OK,
    summary="Удалить соединение по id",
    response_description="Данные удаленного соединения",
)
async def remove_connection(
        connection_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить соединение.

    - **device_id**: внешний ключ устройства
    - **battery_id**: внешний ключ аккумулятора
    - **id**: уникальный идентификатор соединения
    - **user_id**: внешний ключ пользователя, установившего соединение
    """
    connection = await connection_crud.get(
        connection_id, session
    )
    # await check_user_update_delete_rights(connection, user)
    return await connection_crud.remove(
        connection, session
    )
