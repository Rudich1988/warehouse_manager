install:
	poetry install

db_init:
	alembic init warehous_manager/migrations

db_migrate:
	alembic revision --autogenerate

db_upgrade:
	alembic upgrade head

dev:
	uvicorn warehous_manager.app:app --reload