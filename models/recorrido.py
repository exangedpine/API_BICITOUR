from pydantic import BaseModel
from datetime import date, time

class Recorrido(BaseModel):
    fecha: date
    hora: time
    estado: str
    ciudad: str
    km_recorrido: float
    tiempo_est: str
    punto_inicio: str
    costo: float
    foto_zona_visitar: str
    activo: bool

