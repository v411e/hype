FROM python:3-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY ./hype /app

RUN pip install -r requirements.txt

VOLUME /app/config

COPY ./config /app

ENTRYPOINT ["python", "/app/main.py"]