FROM python:3.10-slim-buster

RUN python -m pip install --upgrade pip

RUN mkdir /fastapi_app

WORKDIR  /fastapi_app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod a+x docker/*.sh

# CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
