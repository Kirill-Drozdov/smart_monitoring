from app.core.db.crud.base import CRUDBase
from app.core.db.models import Battery


class CRUDBattery(CRUDBase):
    pass


battery_crud = CRUDBattery(Battery)
