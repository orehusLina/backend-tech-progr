#!/bin/sh

SCRIPT_DIR=$(dirname "$0")
alembic upgrade head
python "${SCRIPT_DIR}/main.py"
