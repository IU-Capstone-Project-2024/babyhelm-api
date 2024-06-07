# Babyhelm

## Run dev fastapi server
```shell
mkdir ./local
cp ./config/config.dev.yaml ./local/config.dev.yaml
```

```shell
poetry run task babyhelm-dev
```

## Setup DB using migrations
```shell
alembic upgrade head
```