
install:
	poetry install

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

unit-test:
	poetry run pytest tests/unit