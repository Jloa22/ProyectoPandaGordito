from db.mongo_conn import get_db
from datetime import datetime

db = get_db()
logs = db["logs"]

def guardar_log(usuario, algoritmo, entrada, salida):
    logs.insert_one({
        "usuario": usuario,
        "algoritmo": algoritmo,
        "entrada": entrada,
        "salida": salida,
        "fecha": datetime.now()
    })
