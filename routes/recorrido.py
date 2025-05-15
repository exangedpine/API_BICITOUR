from fastapi import APIRouter
from models.recorrido import Recorrido
from database.connection import db
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/recorridos")
def crear_recorrido(recorrido: Recorrido):
    data = recorrido.dict()
    
    # Convertir fecha y hora a datetime.datetime
    data["fecha_hora"] = datetime.combine(data["fecha"], data["hora"])
    
    # Eliminar campos individuales (opcional)
    del data["fecha"]
    del data["hora"]

    result = db.recorridos.insert_one(data)
    return {"id": str(result.inserted_id)}

@router.get("/recorridos")
def obtener_recorridos():
    recorridos = list(db.recorridos.find())
    for r in recorridos:
        r["_id"] = str(r["_id"])
        # Convertir fecha_hora a string legible (opcional)
        if "fecha_hora" in r:
            r["fecha_hora"] = r["fecha_hora"].isoformat()
    return recorridos

@router.get("/recorridos/{id}")
def obtener_recorrido(id: str):
    recorrido = db.recorridos.find_one({"_id": ObjectId(id)})
    if recorrido:
        recorrido["_id"] = str(recorrido["_id"])
        if "fecha_hora" in recorrido:
            recorrido["fecha_hora"] = recorrido["fecha_hora"].isoformat()
    return recorrido

@router.put("/recorridos/{id}")
def actualizar_recorrido(id: str, recorrido: Recorrido):
    data = recorrido.dict()
    data["fecha_hora"] = datetime.combine(data["fecha"], data["hora"])
    del data["fecha"]
    del data["hora"]
    result = db.recorridos.update_one({"_id": ObjectId(id)}, {"$set": data})
    return {"modificado": result.modified_count}

@router.delete("/recorridos/{id}")
def eliminar_recorrido(id: str):
    result = db.recorridos.delete_one({"_id": ObjectId(id)})
    return {"eliminado": result.deleted_count}
