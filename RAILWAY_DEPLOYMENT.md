# 📋 Guía de Despliegue en Railway

## ✅ Pasos para desplegar tu bot en Railway

### 1. **Reemplazar `requirements.txt`**
Elimina la línea problemática:
```bash
# ❌ ELIMINA ESTA LÍNEA:
chromadb-huggingface-embeddings==0.0.1

# ✅ MANTÉN ESTAS:
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
pydantic==2.5.3
pydantic-settings==2.1.0
groq==0.4.2
chromadb==0.4.22
huggingface-hub==0.20.3
sentence-transformers==2.2.2
python-dotenv==1.0.0
aiofiles==23.2.1
```

### 2. **Reemplazar Dockerfile**
Usa este Dockerfile simple (NO necesitas docker-compose):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

RUN mkdir -p /app/chroma_data /app/conversations /app/uploads

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. **Configurar `main.py` para Railway**
Asegúrate que el puerto sea dinámico:
```python
if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### 4. **En Railway Dashboard**
- ✅ Crea un nuevo proyecto
- ✅ "Deploy from GitHub" → Selecciona tu repo
- ✅ **NO uses docker-compose**, solo el Dockerfile
- ✅ Ve a "Variables" y añade:
  - `GROQ_API_KEY`: tu clave de Groq
  - `ENVIRONMENT`: production
  - Cualquier otra variable que necesites

### 5. **Eliminar docker-compose.yml** (opcional)
Si tienes `docker-compose.yml`, puedes eliminarlo. Railway lo ignorará si solo quieres 1 servicio.

### 6. **Push a GitHub**
```bash
git add requirements.txt Dockerfile main.py
git commit -m "Fix: Remove invalid chromadb package and optimize for Railway"
git push
```

Railway detectará los cambios y hará un nuevo build automáticamente.

---

## 🔍 Verificar que funciona

Una vez deployado, visita:
```
https://tu-proyecto-en-railway.up.railway.app/api/v1
```

Deberías ver los endpoints disponibles.

---

## ❌ Problemas comunes

### "Build failed"
- Revisa los logs en Railway
- Asegúrate de que `requirements.txt` está en la raíz del repo
- Verifica que `backend/main.py` existe

### "Application crashed"
- Railway te muestra logs en rojo
- Usualmente es por variables de entorno faltantes
- Añade las variables necesarias en "Variables"

### "Port already in use"
- Railway asigna el puerto automáticamente en `$PORT`
- Tu código debe leer: `port = int(os.getenv("PORT", 8000))`

---

## 📚 Estructura esperada del repo:
```
/
├── requirements.txt          ← ✅ Actualizado
├── Dockerfile                ← ✅ Simple (sin compose)
├── backend/
│   ├── main.py              ← ✅ Lee $PORT dinámicamente
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   └── core/
│   │       └── config.py
│   └── ... (resto de carpetas)
└── .env.example              ← Variables necesarias
```

---

¡Listo! Ahora tu bot debería desplegarse en Railway sin problemas 🚀
