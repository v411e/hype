FROM python:3-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY ./hype /app/hype

RUN pip install -r requirements.txt

VOLUME /app/config

RUN mkdir -p /app/config/
RUN mkdir -p /app/secrets/

COPY ./config/* /app/config/

ENTRYPOINT ["python", "-m", "hype"]
