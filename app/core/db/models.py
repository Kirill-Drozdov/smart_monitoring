from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, ForeignKey, String, Text, Integer  # noqa
from sqlalchemy.orm import relationship

from app.core.db.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя."""
    pass


class Device(Base):
    """Модель устройства."""
    type_ = Column(String(100), nullable=False)
    description = Column(Text,)
    # batteries = relationship('Battery', cascade='delete')
    # user_id = Column(Integer, ForeignKey(
    #     'user.id',
    #     name='fk_device_user_id_user',
    # ))
    batteries = relationship(
        "Battery",
        secondary="devicebattery",
        back_populates='devices',
    )

    def __repr__(self):
        return (
            f'Устройство: {self.type_}'
        )


class Battery(Base):
    """Модель аккумулятора."""
    # code = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    devices = relationship(
        "Device",
        secondary="devicebattery",
        back_populates='batteries',
    )
    # type_ = Column(String(100),)
    # power = Column(Integer, nullable=False)
    # voltage = Column(Integer, nullable=False)
    # capacity = Column(Integer, nullable=False)
    # description = Column(Text,)
    # user_id = Column(Integer, ForeignKey(
    #     'user.id',
    #     name='fk_battery_user_id_user',
    # ))

    # def __repr__(self):
    #     return (
    #         f'Аккумулятор: {self.brand} - {self.code}'
    #     )


class DeviceBattery(Base):
    """Модель аккумулятора, подключенного к устройству."""
    device_id = Column(ForeignKey('device.id'), primary_key=True)
    battery_id = Column(ForeignKey('battery.id'), primary_key=True)
