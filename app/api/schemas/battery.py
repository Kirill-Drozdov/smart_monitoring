from pydantic import BaseModel, Extra, Field, validator


class BatteryBase(BaseModel):
    """Базовая схема для аккумулятора."""
    brand: str | None = Field(None, max_length=100)

    @validator('brand')
    def brand_cannot_be_null(cls, value: str):
        if value is None:
            raise ValueError(
                'Поле фирмы не может быть пустым!'
            )
        return value

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class BatteryCreate(BatteryBase):
    """Схема для создания аккумулятора."""
    brand: str = Field(..., max_length=100)


class BatteryUpdate(BatteryBase):
    """Схема для обновления аккумулятора."""
    pass


class BatteryDB(BatteryBase):
    """Схема для получения аккумулятора."""
    id: int
    user_id: int | None

    class Config:
        orm_mode = True
