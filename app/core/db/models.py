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
    user_id = Column(Integer, ForeignKey(
        'user.id',
        name='fk_device_user_id_user',
    ))
    connections = relationship('Connection', cascade='delete')

    def __repr__(self):
        return (
            f'Устройство: {self.type_}'
        )


class Battery(Base):
    """Модель аккумулятора."""
    brand = Column(String(100), nullable=False)
    # code = Column(String(100), nullable=False)
    # devices = relationship(
    #     "Device",
    #     secondary="connection",
    #     back_populates='batteries',
    # )
    user_id = Column(Integer, ForeignKey(
        'user.id',
        name='fk_battery_user_id_user',
    ))
    connections = relationship('Connection', cascade='delete')

    # def __repr__(self):
    #     return (
    #         f'Аккумулятор: {self.brand} - {self.code}'
    #     )


class Connection(Base):
    """Модель аккумулятора, подключенного к устройству."""
    device_id = Column(Integer, ForeignKey(
        'device.id',
        name='fk_device_connection_id_connection',
    ))
    battery_id = Column(Integer, ForeignKey(
        'battery.id',
        name='fk_battery_connection_id_connection',
    ))
    user_id = Column(Integer, ForeignKey(
        'user.id',
        name='fk_connection_user_id_user',
    ))
