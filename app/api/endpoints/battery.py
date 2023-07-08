from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_async_session
from app.core.user import current_user, current_superuser
from app.core.db.crud.battery import battery_crud
from app.core.db.models import User
from app.api.schemas.battery import (
    BatteryCreate,
    BatteryDB,
    BatteryUpdate,
)
from app.core.validators import (
    check_user_update_delete_rights,
)


battery_router = APIRouter()


@battery_router.post(
    '/',
    response_model=BatteryDB,
    status_code=HTTPStatus.CREATED,
    summary="Создать аккумулятор",
    response_description="Информация о созданном аккумуляторе",
)
async def create_new_battery(
        battery: BatteryCreate,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session),
):
    """Создать аккумулятор.

    - **brand**: фирма
    """
    return await battery_crud.create(battery, user, session)


@battery_router.get(
    '/',
    response_model=list[BatteryDB],
    status_code=HTTPStatus.OK,
    summary="Смотреть все аккумуляторы",
    response_description="Список всех аккумуляторов",
)
async def get_all_batteries(
        session: AsyncSession = Depends(get_async_session),
):
    """Смотреть все аккумуляторы.

    - **brand**: фирма
    - **id**: уникальный идентификатор аккумулятора
    - **user_id**: внешний ключ администратора, создавшего аккумулятор
    """
    return await battery_crud.get_multi(session)


@battery_router.get(
    '/{battery_id}',
    response_model=BatteryDB,
    status_code=HTTPStatus.OK,
    summary="Смотреть аккумулятор по id",
    response_description="Данные аккумулятора",

)
async def get_battery(
        battery_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Показать данные аккумулятора.

    - **brand**: фирма
    - **id**: уникальный идентификатор аккумулятора
    - **user_id**: внешний ключ администратора, создавшего аккумулятор
    """
    return await battery_crud.get(
        battery_id, session
    )


@battery_router.patch(
    '/{battery_id}',
    response_model=BatteryDB,
    response_model_exclude_none=True,
    status_code=HTTPStatus.OK,
    summary="Обновить аккумулятор по id",
    response_description="Данные обновленного аккумулятора",
)
async def partially_update_battery(
        battery_id: int,
        obj_in: BatteryUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Обновить аккумулятор.

    - **brand**: фирма
    """
    battery = await battery_crud.get(
        battery_id, session
    )
    return await battery_crud.update(
        battery, obj_in, session
    )


@battery_router.delete(
    '/{battery_id}',
    response_model=BatteryDB,
    response_model_exclude_none=True,
    status_code=HTTPStatus.OK,
    summary="Удалить аккумулятор по id",
    response_description="Данные удаленного аккумулятор",
)
async def remove_battery(
        battery_id: int,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить аккумулятор.

    - **brand**: фирма
    - **id**: уникальный идентификатор аккумулятора
    - **user_id**: внешний ключ администратора, создавшего аккумулятор
    """
    battery = await battery_crud.get(
        battery_id, session
    )
    await check_user_update_delete_rights(battery, user)
    return await battery_crud.remove(
        battery, session
    )
