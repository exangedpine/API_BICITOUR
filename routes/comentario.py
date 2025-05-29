from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete
from models.comentario import ComentarioModel
from schemas import ComentarioSchema
from database.connection import get_db  # función async para obtener sesión

router = APIRouter(prefix="/comentarios", tags=["Comentarios"], responses={404: {"description": "No encontrado"}})

# End Points Comentario
# Petición POST
# Esta función crea un nuevo comentario.
@router.post("/", response_model=ComentarioSchema.Comentario, status_code=status.HTTP_201_CREATED)
async def crear_comentario(
    comentario: ComentarioSchema.ComentarioCreate,
    db: AsyncSession = Depends(get_db)
):
    # Crear instancia del modelo con datos
    db_comentario = ComentarioModel(
        comentario = comentario.comentario,
        calificacion = comentario.calificacion,
        id_inscripcion = comentario.id_inscripcion
    )

    # Agregar y confirmar cambios async
    db.add(db_comentario)
    await db.commit()
    await db.refresh(db_comentario)  # Refresca para obtener id generado

    return db_comentario

# Función para obtener el usuario individualmente.
async def get_comentario(
    id_comentario: int,
    db: AsyncSession
):
    result = await db.execute(
        select(ComentarioModel).where(ComentarioModel.id_inscripcion == id_comentario)
    )
    return result.scalar_one_or_none()

# Petición GET
# Esta función obtiene todos los datos de la tabla recorridos.
@router.get("/", response_model=list[ComentarioSchema.Comentario], status_code=status.HTTP_200_OK)
async def read_comentario(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(ComentarioModel).offset(skip).limit(limit)
    )

    comentarios = result.scalars().all()

    return comentarios


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

# Función para eliminar un comentario
@router.delete("/{id_comentario}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comentario(id_comentario: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        delete(ComentarioModel)
        .where(ComentarioModel.id_comentario == id_comentario)
        .execution_options(synchronize_session="fetch")
    )

    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND)