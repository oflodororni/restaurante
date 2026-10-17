.PHONY: run test lint format init-db seed migrate

run:
FLASK_APP=run.py flask run

test:
pytest

lint:
ruff check app tests
black --check app tests

format:
black app tests
ruff check --fix app tests

init-db:
FLASK_APP=run.py flask init-db

seed:
FLASK_APP=run.py flask seed

migrate:
FLASK_APP=run.py flask db upgrade
