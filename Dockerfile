FROM python:3.11-slim-buster

ARG POETRY_AUTH
ARG CI_COMMIT_SHORT_SHA="-"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.3 \
    CI_COMMIT_SHORT_SHA=$CI_COMMIT_SHORT_SHA

RUN apt-get update \
    && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p ~/.config/pypoetry/ \
    && echo "${POETRY_AUTH}" > ~/.config/pypoetry/auth.toml \
    && pip install -U "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false \
    && mkdir -p /app

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./README.md ./alembic.ini /app/
COPY ./babyhelm /app/babyhelm
COPY ./config /app/local
COPY ./alembic /app/alembic

RUN poetry install --no-interaction --no-ansi

RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "babyhelm.app", "--host", "0.0.0.0", "--config", "/app/local/config.dev.yaml", "--log-level", "info"]
