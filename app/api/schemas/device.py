from pydantic import BaseModel, Extra, Field, validator


class DeviceBase(BaseModel):
    """Базовая схема для устройства."""
    type_: str | None = Field(None, max_length=100)
    description: str | None

    @validator('type_')
    def type_cannot_be_null(cls, value: str):
        if value is None:
            raise ValueError(
                'Поле "тип" не может быть пустым!'
            )
        return value

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class DeviceCreate(DeviceBase):
    """Схема для создания устройства."""
    type_: str = Field(..., max_length=100)


class DeviceUpdate(DeviceBase):
    """Схема для обновления устройства."""
    pass


class DeviceDB(DeviceBase):
    """Схема для получения устройства."""
    id: int
    user_id: int | None

    class Config:
        orm_mode = True
