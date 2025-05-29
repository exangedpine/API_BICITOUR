from fastapi import FastAPI
from routes import recorrido, inscripcion
from fastapi.staticfiles import StaticFiles

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

# Montar carpeta estática
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(recorrido.router)
app.include_router(inscripcion.router)

