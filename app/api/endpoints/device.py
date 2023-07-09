from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_async_session
from app.core.user import current_user, current_superuser
from app.core.db.crud.connection import connection_crud
from app.core.db.crud.device import device_crud
from app.core.db.models import User
from app.api.schemas.connection import ConnectionDB
from app.api.schemas.device import (
    DeviceCreate,
    DeviceDB,
    DeviceUpdate,
)
from app.core.validators import (
    check_user_update_delete_rights,
)


device_router = APIRouter()


@device_router.post(
    '/',
    response_model=DeviceDB,
    status_code=HTTPStatus.CREATED,
    summary='Создать устройство',
    response_description='Информация о созданном устройстве',
)
async def create_new_device(
        device: DeviceCreate,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session),
):
    """Создать устройство.

    - **type_**: тип
    - **description**: описание
    """
    return await device_crud.create(device, user, session)


@device_router.get(
    '/',
    response_model=list[DeviceDB],
    status_code=HTTPStatus.OK,
    summary='Смотреть все устройства',
    response_description='Список всех устройств',
)
async def get_all_devices(
        session: AsyncSession = Depends(get_async_session),
):
    """Смотреть все устройства.

    - **type_**: тип
    - **description**: описание
    - **id**: уникальный идентификатор устройства
    - **user_id**: внешний ключ администратора, создавшего устройство
    """
    return await device_crud.get_multi(session)


@device_router.get(
    '/{device_id}',
    response_model=DeviceDB,
    status_code=HTTPStatus.OK,
    summary='Смотреть устройство по id',
    response_description='Данные устройства',

)
async def get_device(
        device_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Показать данные устройства.

    - **type_**: тип
    - **description**: описание
    - **id**: уникальный идентификатор устройства
    - **user_id**: внешний ключ администратора, создавшего устройство
    """
    return await device_crud.get(
        device_id, session
    )


@device_router.patch(
    '/{device_id}',
    response_model=DeviceDB,
    response_model_exclude_none=True,
    status_code=HTTPStatus.OK,
    summary='Обновить устройство по id',
    response_description='Данные обновленного устройства',
)
async def partially_update_device(
        device_id: int,
        obj_in: DeviceUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Обновить устройство.

    - **type_**: тип
    - **description**: описание
    """
    device = await device_crud.get(
        device_id, session
    )
    return await device_crud.update(
        device, obj_in, session
    )


@device_router.delete(
    '/{device_id}',
    response_model=DeviceDB,
    response_model_exclude_none=True,
    status_code=HTTPStatus.OK,
    summary='Удалить устройство по id',
    response_description='Данные удаленного устройства',
)
async def remove_device(
        device_id: int,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить устройство.

    - **type_**: тип
    - **description**: описание
    - **id**: уникальный идентификатор устройства
    - **user_id**: внешний ключ администратора, создавшего устройство
    """
    device = await device_crud.get(
        device_id, session
    )
    await check_user_update_delete_rights(device, user)
    return await device_crud.remove(
        device, session
    )


@device_router.delete(
    '/{device_id}/disconnect',
    response_model=list[ConnectionDB],
    status_code=HTTPStatus.OK,
    summary='Отсоединить устройство',
    response_description='Данные удаленного соединения',
)
async def disconnect_device(
        device_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Отсоединить устройство.

    - **device_id**: внешний ключ устройства
    - **battery_id**: внешний ключ аккумулятора
    - **id**: уникальный идентификатор соединения
    - **user_id**: внешний ключ пользователя, установившего соединение
    - **created_at**: время установки соединение
    """
    connections = await connection_crud.get_connections_by_device_id(
        device_id, session
    )
    response = []
    for item in connections:
        connection = await connection_crud.remove(
            item, session
        )
        response.append(connection)
    return response
