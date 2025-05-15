from fastapi import APIRouter
from models.recorrido import Recorrido
from database.connection import db
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/recorridos")
async def crear_recorrido(recorrido: Recorrido):
    data = recorrido.dict()
    data["fecha_hora"] = datetime.combine(data["fecha"], data["hora"])
    del data["fecha"]
    del data["hora"]
    
    result = await db.recorridos.insert_one(data)
    return {"id": str(result.inserted_id)}

@router.get("/recorridos")
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
