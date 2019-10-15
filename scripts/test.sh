#!/usr/bin/env bash
set -e

use_tag="tiangolo/uvicorn-gunicorn-starlette:$NAME"

docker build -t "$use_tag" "$BUILD_PATH"
pytest tests
