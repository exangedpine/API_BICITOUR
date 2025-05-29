from pydantic import BaseModel, EmailStr # EmailStr: formato string correcto de un correo.
from typing import List, Optional
from datetime import datetime, date, time

class ComentarioBase(BaseModel):
    comentario: str
    calificacion: str
    id_inscripcion: int

class ComentarioCreate(ComentarioBase):
    pass

class Comentario(ComentarioBase):
    id_inscripcion: int
    created_at: datetime

    class Config:
        from_attributes=True
