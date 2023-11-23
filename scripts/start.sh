#!/usr/bin/env bash

set -e

edgedb migrate --dsn="${EDGEDB_DSN}" || true

uvicorn app.main:app --host 0.0.0.0 --port 80