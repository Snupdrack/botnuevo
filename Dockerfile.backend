# 1. Usar una imagen ligera de Python
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Instalar dependencias del sistema necesarias para ChromaDB y utilidades
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiar requirements desde tu carpeta backend e instalar
# (Asumiendo que tu carpeta se llama 'backend' en GitHub)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar TODO el contenido de la carpeta backend a la raíz /app
# Esto hace que main.py quede en /app/main.py
COPY backend/ .

# 6. Crear los directorios de persistencia para que no den error de escritura
RUN mkdir -p /app/chroma_data /app/conversations /app/uploads

# 7. Configuraciones de entorno
ENV PYTHONUNBUFFERED=1
ENV CHROMA_PERSIST_DIR=/app/chroma_data

# 8. Railway asigna el puerto automáticamente en la variable $PORT
# Exponemos el 8080 que es el estándar de Railway, pero el comando final manda.
EXPOSE 8080

# 9. Comando de inicio optimizado
# Usamos 'sh -c' para que interprete correctamente la variable de puerto de Railway
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]