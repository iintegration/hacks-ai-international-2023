FROM edgedb/edgedb-cli as edgedb-cli
FROM python:3.11-slim as play

WORKDIR /usr/src/app

ENV DEBIAN_FRONTEND=noninteractive \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PYTHONPATH="${PYTHONPATH}:/app" \
  PATH="/usr/src/app/scripts:${PATH}"

RUN apt update \
    && apt-get install -y --no-install-recommends git gcc python3-dev build-essential wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip poetry && \
    poetry config virtualenvs.create false

RUN wget -q -O /cache/hf/model-q4_K.gguf https://huggingface.co/IlyaGusev/saiga_mistral_7b_gguf/resolve/main/model-q4_K.gguf

COPY pyproject.toml poetry.lock /usr/src/app/
RUN poetry install -n --with=background \
    && apt-get purge -y --auto-remove gcc python3-dev build-essential wget git

COPY scripts /usr/src/app/scripts/
RUN chmod +x /usr/src/app/scripts/*

COPY --from=edgedb-cli /usr/bin/edgedb /usr/bin/
COPY dbschema /usr/src/app/dbschema/
COPY edgedb.toml /usr/src/app/

COPY ./app /usr/src/app/app

STOPSIGNAL SIGINT
ENTRYPOINT [ "start-worker.sh" ]