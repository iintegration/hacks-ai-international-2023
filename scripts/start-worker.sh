#!/usr/bin/env bash

set -e

mkdir -p /cache/saiga && \
  wget -c -O /cache/saiga/model-q4_K.gguf https://huggingface.co/IlyaGusev/saiga_mistral_7b_gguf/resolve/main/model-q4_K.gguf

edgedb migrate --dsn="${EDGEDB_DSN}" || true

arq app.background.worker.BackgroundSettings