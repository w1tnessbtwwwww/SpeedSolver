dev:
	poetry run uvicorn main:api --reload --port 8000

rev:
	poetry run alembic revision --autogenerate

mig:
	poetry run alembic upgrade head

kill:
	taskkill /f /im python.exe

migration:
	poetry run alembic revision --autogenerate
	poetry run alembic upgrade head