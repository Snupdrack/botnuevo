FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements desde la subcarpeta
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPIAR TODO EL CONTENIDO DE BACKEND A LA RAÍZ DE /APP
COPY backend/ .

# Crear directorios para persistencia
RUN mkdir -p /app/chroma_data /app/conversations /app/uploads

ENV PYTHONUNBUFFERED=1
ENV CHROMA_PERSIST_DIR=/app/chroma_data
ENV PORT=8000

# El puerto DEBE ser dinámico para Railway
EXPOSE 8000

# CORRECCIÓN AQUÍ: Si tu main.py está en la raíz de la carpeta backend,
# el comando debe ser "main:app", no "app.main:app"
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}