from pydantic import BaseModel, EmailStr # EmailStr: formato string correcto de un correo.
from typing import List, Optional
from datetime import datetime, date, time

class RecorridoBase(BaseModel):
    fecha_creacion: date
    hora: Optional[time] = None
    estado: str
    ciudad: str
    km_recorrido: float
    tiempo_est: Optional[str] = None
    punto_inicio: Optional[str] = None
    costo: Optional[float] = None
    foto_zona_visitar: Optional[str] = None
    activo: Optional[bool] = None

class RecorridoCreate(RecorridoBase):
    pass

class Recorrido(RecorridoBase):
    id_recorrido: int
    created_at: datetime

    # Conversión del schema a JSON
    class Config:
        from_attributes: True 
        
        
class RecorridoUpdate(BaseModel):
    fecha_creacion: Optional[date] = None
    hora: Optional[time] = None
    estado: Optional[str] = None
    ciudad: Optional[str] = None
    km_recorrido: Optional[float] = None
    tiempo_est: Optional[str] = None
    punto_inicio: Optional[str] = None
    costo: Optional[float] = None
    foto_zona_visitar: Optional[str] = None
    activo: Optional[bool] = None




