from pydantic import BaseModel


class ConnectionCreate(BaseModel):
    """Схема для создания устройства."""
    device_id: int
    battery_id: int


# class DeviceUpdate(ConnectionBase):
#     """Схема для обновления устройства."""
#     pass


class ConnectionDB(ConnectionCreate):
    """Схема для получения устройства."""
    id: int
    user_id: int

    class Config:
        orm_mode = True
