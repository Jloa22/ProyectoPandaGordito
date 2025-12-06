from db.mongo_conn import get_db
from datetime import datetime

db = get_db()

if db:
    logs = db["logs"]
else:
    print("❌ No hay DB, logs no cargado")
    logs = None


def guardar_log(usuario, algoritmo, entrada, salida):
    if logs is None:
        print("❌ No se puede guardar log (DB no disponible)")
        return

    logs.insert_one({
        "usuario": usuario,
        "algoritmo": algoritmo,
        "entrada": entrada,
        "salida": salida,
        "fecha": datetime.now()
    })
