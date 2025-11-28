FROM python:3.10-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache curl libffi-dev build-base && \
    curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY ./app/pyproject.toml ./app/poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi --only main

COPY ./app ./
RUN apk add --no-cache dos2unix && \
    find ./__scripts -type f -exec dos2unix {} \; && \
    chmod +x ./__scripts/*

FROM python:3.10-alpine AS runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app ./

ENTRYPOINT ["./__scripts/entrypoint.sh"]
