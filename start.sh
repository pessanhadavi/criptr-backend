#!/bin/bash
echo "Aguardando o banco de dados ficar disponível..."

# Espera até a porta 3306 do serviço mariadb estar disponível
while ! nc -z mariadb 3306; do
  sleep 1
done

echo ">> Aplicando migrações Alembic..."
alembic upgrade head

echo ">> Iniciando servidor FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
