install-dev:
	pip install --no-cache-dir -U pip poetry
	poetry lock --no-update
	poetry install --all-extras

format:
	poetry run ruff check . --select I --fix
	poetry run ruff format .