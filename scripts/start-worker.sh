#!/usr/bin/env bash

set -e

edgedb migrate --dsn="${EDGEDB_DSN}" || true

arq app.background.worker.BackgroundSettings