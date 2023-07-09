from datetime import datetime

from pydantic import BaseModel


class ConnectionCreate(BaseModel):
    """Схема для создания соединения."""
    device_id: int
    battery_id: int


class ConnectionDB(ConnectionCreate):
    """Схема для получения соединения."""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
