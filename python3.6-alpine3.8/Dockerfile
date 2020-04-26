FROM tiangolo/uvicorn-gunicorn:python3.6-alpine3.8

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

RUN pip --no-cache-dir install starlette

COPY ./app /app
