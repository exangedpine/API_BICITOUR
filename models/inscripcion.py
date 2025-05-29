import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Float, DateTime, Date, Time # Tipos de datos
from sqlalchemy.sql import func
from database.connection import Base
from sqlalchemy.orm import relationship

class InscripcionModel(Base):
    __tablename__= "inscripciones"
    id_inscripcion = Column(Integer, primary_key=True, index=True)
    id_recorrido = Column(Integer, ForeignKey("recorridos.id_recorrido"))
    nombre = Column(String)
    apellidos = Column(String)
    email = Column(String)
    telefono = Column(Integer)
    ciudad = Column(String)
    estado = Column(String)

    # Clave única para verificar la inscripción
    clave_unica = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))

    recorrido = relationship("RecorridoModel")
