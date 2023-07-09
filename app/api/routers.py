from fastapi import APIRouter

from app.api.endpoints.battery import battery_router
from app.api.endpoints.connection import connection_router
from app.api.endpoints.device import device_router
from app.api.endpoints.user import user_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(
    battery_router,
    prefix='/batteries',
    tags=['Battery'],
)
main_router.include_router(
    device_router,
    prefix='/devices',
    tags=['Device'],
)
main_router.include_router(
    connection_router,
    prefix='/connections',
    tags=['Connection'],
)
