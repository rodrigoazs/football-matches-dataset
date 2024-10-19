.PHONY: tests

PROJECT_SLUG := cdp_parser

install-dev:
	pip install --no-cache-dir -U pip poetry
	poetry lock --no-update
	poetry install --all-extras

format:
	poetry run ruff check . --select I --fix
	poetry run ruff format .

check:
	poetry run ruff format . --check
	poetry run ruff check $(PROJECT_SLUG)

tests:
	poetry run python -m pytest -v tests -m "not (slow or integration or system)"

cov-tests:
	poetry run python -m pytest -v tests --cov $(PROJECT_SLUG) --cov-branch --cov-fail-under=60 --cov-report term-missing --disable-warnings
