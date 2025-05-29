from fastapi import FastAPI
from routes import recorrido, inscripcion
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Importa todos los modelos para que se registren en metadata
from models.recorrido import RecorridoModel
from models.inscripcion import InscripcionModel
from models.comentario import ComentarioModel

from database.connection import engine, Base

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Define el path correcto a la carpeta "static"
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Montar carpeta estática
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(recorrido.router)
app.include_router(inscripcion.router)
