#!/bin/sh
set -eux

SCRIPT_DIR=$(dirname "$0")
# Enable new docker build infrastructure (BuildKit)
export DOCKER_BUILDKIT=1
# Disable `docker scan` promo messages after each build
export DOCKER_SCAN_SUGGEST="${DOCKER_SCAN_SUGGEST:-false}"
PROJECT="${PROJECT:-fastapi_app}"
TAG="${TAG:-${PROJECT}:latest}"

docker build \
    --progress plain \
    --tag "${TAG}" \
    "$@" \
    "${SCRIPT_DIR}"
