## SmartMonitoring

### О проекте
Данный проект представляет собой сервис для удобного мониторинга работы аккумуляторов.


### Технологии
```
python==3.10
alembic==1.7.7
fastapi-users-db-sqlalchemy==4.0.0
fastapi==0.78.0
uvicorn==0.17.6
SQLAlchemy==1.4.36
```
> **Note**:
> Подробный список зависимостей представлен в файле `requirements.txt`.

### Установка

1. Клонировать репозиторий и перейти в него в командной строке:

    ```shell
    git clone git@github.com:Kirill-Drozdov/smart_monitoring.git
    ```

    ```shell
    cd smart_monitoring
    ```

2. Cоздать и активировать виртуальное окружение с `python 3.10`:

    ```shell
    python3 -m venv venv
    ```

    * Если у вас Linux/macOS

        ```
        source venv/bin/activate
        ```

    * Если у вас windows

        ```
        source venv/scripts/activate
        ```

3. Установить зависимости из файла `requirements.txt`:

    ```shell
    python3 -m pip install --upgrade pip
    ```

    ```shell
    pip install -r requirements.txt
    ```

4. Создать файл `.env` и заполнить его по примеру
из файла `.env.template`.


### Запуск

1. Выполнить запуск контейнера с `PostgreSQL`:

    ```shell
    docker-compose up -d
    ```
    > **Warning**:
    > Убедитесь, что на вашем ПК установлен `Docker`.
    > Подробнее об установке: https://www.docker.com/products/docker-desktop/

2. Применить миграции базы данных:

    ```shell
    alembic upgrade head
    ```
    > **Warning**:
    > Переходить к этому шагу только после успешного запуска контейнера с `PostgreSQL`!

3. Запустить проект:

    ```shell
    uvicorn app.main:app
    ```
    > **Note**:
    > Вы можете запускать проект в режиме отладки, добавив флаг --reload.
   
    > **Note**:
    > При первом запуске проекта будет автоматически создан суперпользователь (админ).
    > Данные для входа под админом содержатся в константах `FIRST_SUPERUSER_EMAIL` и `FIRST_SUPERUSER_PASSWORD` в файле `.env`.


### Использование
После выполнения инструкций, описанных в разделе
"[Установка и Запуск](#установка-и-запуск)", вы сможете получить
доступ к полной спецификации по стандарту OpenAPI, перейдя по адресу http://localhost:8000/docs


### Об авторе проекта:
Проект выполнил [Дроздов К.С.](https://github.com/Kirill-Drozdov)
