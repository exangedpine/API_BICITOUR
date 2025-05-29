from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Float, DateTime, Date, Time # Tipos de datos
from sqlalchemy.orm import relationship # Sirve para definir relación entre clases.
from sqlalchemy.sql import func # Nos permite llamar a funciones sql desde python.
from database.connection import Base # Indica que modelos se debe usar como tablas.

class RecorridoModel(Base):
    __tablename__="recorridos"
    id_recorrido = Column(Integer, primary_key=True, index=True)
    fecha_creacion = Column(Date, server_default=func.current_date()) 
    hora = Column(Time, server_default=func.current_time())
    estado = Column(String)
    ciudad = Column(String)
    km_recorrido = Column(Float)
    tiempo_est = Column(String)
    punto_inicio = Column(String)
    costo = Column(Float)
    foto_zona_visitar = Column(String, nullable=True)
    activo = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())







