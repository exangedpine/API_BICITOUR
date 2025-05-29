from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete
from models.inscripcion import InscripcionModel
from schemas import InscripcionSchema
from database.connection import get_db  # función async para obtener sesión

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"], responses={404: {"description": "No encontrado"}})

# End Points Recorrido
# Petición POST
# Esta función crea un nuevo recorrido.
@router.post("/", response_model=InscripcionSchema.Inscripcion, status_code=status.HTTP_201_CREATED)
async def crear_inscripcion(
    inscripcion: InscripcionSchema.InscripcionCreate,
    db: AsyncSession = Depends(get_db)
):
    # Crear instancia del modelo con datos
    db_inscripcion = InscripcionModel(
        nombre = inscripcion.nombre,
        apellidos = inscripcion.apellidos,
        email = inscripcion.email,
        telefono = inscripcion.telefono,
        ciudad = inscripcion.ciudad,
        estado = inscripcion.estado,
        id_recorrido = inscripcion.id_recorrido
    )

    # Agregar y confirmar cambios async
    db.add(db_inscripcion)
    await db.commit()
    await db.refresh(db_inscripcion)  # Refresca para obtener id generado

    return db_inscripcion

# Función para obtener el usuario individualmente.
async def get_inscripcion(
    id_inscripcion: int,
    db: AsyncSession
):
    result = await db.execute(
        select(InscripcionModel).where(InscripcionModel.id_inscripcion == id_inscripcion)
    )
    return result.scalar_one_or_none()

# Petición GET
# Esta función obtiene todos los datos de la tabla recorridos.
@router.get("/", response_model=list[InscripcionSchema.Inscripcion], status_code=status.HTTP_200_OK)
async def read_inscripcion(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(InscripcionModel).offset(skip).limit(limit)
    )

    inscripciones = result.scalars().all()

    return inscripciones

"""
# Función para actualizar un recorrido.
@router.put("/{id_inscripcion}", status_code=status.HTTP_204_NO_CONTENT)
async def update_recorrido(
    inscripcion: InscripcionSchema.InscripcionCreate,
    id_inscripcion: int,
    db: AsyncSession = Depends(get_db)
):
    inscripcion = await get_inscripcion(id_inscripcion, db)
    
    if not inscripcion:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    result = await db.execute(
        update(InscripcionModel)
        .where(InscripcionModel.id == id_inscripcion)
        .values(
            nombre = inscripcion.nombre,
            apellidos = inscripcion.apellidos,
            email = inscripcion.email,
            telefono = inscripcion.telefono,
            ciudad = inscripcion.ciudad,

        )
        .execution_options(synchronize_session="fetch")
    )

    await db.commit()

    return {"msg": "Recorrido actualizado","filas_modificadas":result.rowcount}
"""

# Función para eliminar un recorrido.
@router.delete("/{id_inscripcion}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inscripcion(id_inscripcion: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        delete(InscripcionModel)
        .where(InscripcionModel.id_inscripcion == id_inscripcion)
        .execution_options(synchronize_session="fetch")
    )

    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    