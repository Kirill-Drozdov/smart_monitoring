from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Настройки проекта."""
    APP_TITLE: str = 'Title'
    APP_DESCRIPTION: str = 'Description'
    SECRET: str = 'letspythonizetheworld:)'
    FIRST_SUPERUSER_EMAIL: EmailStr = 'admin@ya.ru'
    FIRST_SUPERUSER_PASSWORD: Optional[str] = None

    # Настройки взаимодействия с БД
    POSTGRES_DB: str  # Имя базы данных
    POSTGRES_USER: str  # имя пользователя ля для подключения к БД
    POSTGRES_PASSWORD: str  # пароль для подключения к БД
    DB_HOST: str  # название сервиса (контейнера)
    DB_PORT: str  # порт для подключения к БД

    @property
    def database_url(self) -> str:
        """Получить ссылку для подключения к DB."""
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = '.env'


settings = Settings()
