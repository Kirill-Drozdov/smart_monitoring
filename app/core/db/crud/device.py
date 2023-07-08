from app.core.db.crud.base import CRUDBase
from app.core.db.models import Device


class CRUDDevice(CRUDBase):
    pass


device_crud = CRUDDevice(Device)
