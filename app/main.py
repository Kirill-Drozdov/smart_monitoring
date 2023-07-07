from fastapi import FastAPI

from app.api.routers import main_router
from app.core.settings import settings
from app.core.db.init_db import create_first_superuser

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
