run:
	uv run main.py

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix --no-unsafe-fixes

format:
	uv run ruff format --check --diff && uv run ruff check --select I

format-fix:
	uv run ruff format && uv run ruff check --select I --fix

mypy:
	uv run mypy .

test:
	uv run pytest .
