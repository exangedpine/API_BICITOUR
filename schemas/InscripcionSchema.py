from pydantic import BaseModel, EmailStr # EmailStr: formato string correcto de un correo.
from typing import List, Optional
from datetime import datetime, date, time

class InscripcionBase(BaseModel):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: int
    ciudad: str
    estado: str
    id_recorrid: int


class InscripcionCreate(InscripcionBase):
    pass

class Inscripcion(InscripcionBase):
    id_inscripcion: int
    clave_unica: str

    class Config:
        from_attributes=True


