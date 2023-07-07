from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models import TemplateModel
from app.core.db.models import User


async def check_field_is_unique(
        fild_to_check: str,
        session: AsyncSession,
) -> None:
    """Проверка поля на уникальность."""
    exists_criteria = (
        select(TemplateModel).where(
            TemplateModel.field == fild_to_check
        ).exists()
    )
    db_advert_exists = await session.execute(
        select(True).where(
            exists_criteria
        )
    )
    db_advert_exists = db_advert_exists.scalars().first()
    if db_advert_exists:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Придумайте уникальное описание объявления!',
        )


async def check_user_update_delete_rights(
        obj_db,
        user: User,
):
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
):
    """Проверка прав пользователя на создание записи."""
    if obj_db.user_id == user.id and not user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='У Вас нет прав на осуществление данного действия!'
        )
    return obj_db
