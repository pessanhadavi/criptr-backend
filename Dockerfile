FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["./start.sh"]
