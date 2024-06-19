
install:
	poetry install

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

unit-tests:
	poetry run pytest tests/unit
