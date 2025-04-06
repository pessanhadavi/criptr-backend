#!/bin/bash

echo ">> Aplicando migrações Alembic..."
alembic upgrade head

echo ">> Iniciando servidor FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
