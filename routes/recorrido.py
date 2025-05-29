from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.recorrido import RecorridoModel
from schemas import RecorridoSchema
from database.connection import get_db  # función async para obtener sesión

import os
import shutil
from uuid import uuid4

router = APIRouter(prefix="/recorridos", tags=["Recorridos"], responses={404: {"msg":"No encontrado"}})

# End Points Recorrido
# Petición POST
# Esta función crea un nuevo recorrido.
@router.post("/", response_model=RecorridoSchema.Recorrido, status_code=status.HTTP_201_CREATED)
async def crear_recorrido(
    fecha_creacion: str = Form(...),
    estado: str = Form(...),
    ciudad: str = Form(...),
    km_recorrido: float = Form(...),
    foto_zona_visitar: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Guardar la imagen en una carpeta local
    nombre_archivo = f"{uuid4().hex}_{foto_zona_visitar.filename}"
    ruta_guardado = f"static/recorridos/{nombre_archivo}"  # Asegúrate de crear esta carpeta
    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

    with open(ruta_guardado, "wb") as buffer:
        shutil.copyfileobj(foto_zona_visitar.file, buffer)

    # Crear instancia del modelo con datos
    db_recorrido = RecorridoModel(
        fecha_creacion=fecha_creacion,
        estado=estado,
        ciudad=ciudad,
        km_recorrido=km_recorrido,
        foto_zona_visitar=ruta_guardado  # o solo nombre_archivo si solo guardarás la referencia
    )

    # Guardar en la base de datos
    db.add(db_recorrido)
    await db.commit()
    await db.refresh(db_recorrido)

    return db_recorrido

# Función para obtener el usuario individualmente.
async def get_recorrido(
    id_recorrido: int,
    db: AsyncSession
):
    result = await db.execute(
        select(RecorridoModel).where(RecorridoModel.id_recorrido == id_recorrido)
    )
    return result.scalar_one_or_none()

# Petición GET
# Esta función obtiene todos los datos de la tabla recorridos.
@router.get("/", response_model=list[RecorridoSchema.Recorrido], status_code=status.HTTP_200_OK)
async def read_recorrido(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(RecorridoModel).offset(skip).limit(limit)
    )

    recorridos = result.scalars().all()

    return recorridos

# Función para actualizar un recorrido.
@router.put("/{id_recorrido}", status_code=status.HTTP_204_NO_CONTENT)
async def update_recorrido(
    recorrido: RecorridoSchema.RecorridoUpdate,
    id_recorrido: int,
    db: AsyncSession = Depends(get_db)
):
    recorrido = await get_recorrido(id_recorrido, db)
    
    if not recorrido:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    result = await db.execute(
        update(RecorridoModel)
        .where(RecorridoModel.id_recorrido == id_recorrido)
        .values(
            fecha_creacion = recorrido.fecha_creacion,
            estado = recorrido.estado,
            ciudad = recorrido.ciudad,
            km_recorrido = recorrido.km_recorrido
        )
        .execution_options(synchronize_session="fetch")
    )

    await db.commit()

    return {"msg": "Recorrido actualizado","filas_modificadas":result.rowcount}


"""
# Función para eliminar un recorrido.
@router.delete("/{id_recorrido}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recorrido(id_recorrido: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        delete(Recorrido)
        .where(Recorrido.id == id_recorrido)
        .execution_options(synchronize_session="fetch")
    )

    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
"""
    

""" @router.get("/recorridos")
async def obtener_recorridos():
    recorridos_cursor = db.recorridos.find()
    recorridos = await recorridos_cursor.to_list(length=None)

    for r in recorridos:
        r["_id"] = str(r["_id"])
        if "fecha_hora" in r:
            r["fecha_hora"] = r["fecha_hora"].isoformat()
    return recorridos

@router.get("/recorridos/{id}")
async def obtener_recorrido(id: str):
    recorrido = await db.recorridos.find_one({"_id": ObjectId(id)})
    if recorrido:
        recorrido["_id"] = str(recorrido["_id"])
        if "fecha_hora" in recorrido:
            recorrido["fecha_hora"] = recorrido["fecha_hora"].isoformat()
    return recorrido

@router.put("/recorridos/{id}")
async def actualizar_recorrido(id: str, recorrido: Recorrido):
    data = recorrido.dict()
    data["fecha_hora"] = datetime.combine(data["fecha"], data["hora"])
    del data["fecha"]
    del data["hora"]

    result = await db.recorridos.update_one({"_id": ObjectId(id)}, {"$set": data})
    return {"modificado": result.modified_count}

@router.delete("/recorridos/{id}")
async def eliminar_recorrido(id: str):
    result = await db.recorridos.delete_one({"_id": ObjectId(id)})
    return {"eliminado": result.deleted_count}
"""