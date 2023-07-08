from app.core.db.crud.base import CRUDBase
from app.core.db.models import Connection


class CRUDConnection(CRUDBase):
    pass


connection_crud = CRUDConnection(Connection)
