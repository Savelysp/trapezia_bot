FROM python:3.12-alpine3.20

ARG APP_PATH=/opt

WORKDIR $APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

COPY requirements.txt $APP_PATH/requirements.txt

RUN apk add build-base && \
    pip install --no-cache-dir --upgrade -r $APP_PATH/requirements.txt
