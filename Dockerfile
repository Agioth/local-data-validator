FROM python:3.10-slim

WORKDIR /app

# Instala dependências do sistema necessárias para o psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Porta do Dash
EXPOSE 8050

CMD ["python", "app_dashboard.py"]