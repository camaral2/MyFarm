FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependências do sistema (ajuste se usar psycopg2 "ortodoxo")
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements*.txt ./
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi && \
    if [ -f requirements-prod.txt ]; then pip install -r requirements-prod.txt; fi

# Copia apenas o código da aplicação
COPY app ./app

EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--proxy-headers"]
