#!/usr/bin/env bash

set -e

edgedb migrate --dsn="${EDGEDB_DSN}" || true

python -m app