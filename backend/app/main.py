from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import settings
import os

app = FastAPI(
    title="SynkBot API",
    description="API del asistente virtual de SynkData",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router, prefix="/api/v1")

# Health check endpoint (requerido por Railway)
@app.get("/health")
async def health():
    return {"status": "ok"}

# Startup
@app.on_event("startup")
async def startup():
    # Crear directorios necesarios
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)
    os.makedirs("./conversations", exist_ok=True)
    os.makedirs("./uploads", exist_ok=True)
    print("🚀 SynkBot API iniciado!")

if __name__ == "__main__":
    import uvicorn
    # Railway asigna dinámicamente el puerto en la variable PORT
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)