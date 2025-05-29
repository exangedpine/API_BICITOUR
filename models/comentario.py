import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime # Tipos de datos
from sqlalchemy.sql import func
from database.connection import Base
from sqlalchemy.orm import relationship

class ComentarioModel(Base):
    __tablename__="comentarios"
    id_comentario = Column(Integer, primary_key=True, index=True)
    comentario = Column(String)
    calificacion = Column(String)
    id_inscripcion = Column(Integer, ForeignKey("inscripciones.id_inscripcion"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    inscripcion = relationship("InscripcionModel")
