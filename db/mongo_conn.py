print("🔵 Railway detecta mongo_conn.py iniciando...")

import os
from pymongo import MongoClient

def get_db():
    # 1. Railway NO usa st.secrets, solo variables de entorno
    mongo_uri = os.getenv("MONGO_URI")

    print("🔵 Cargando MONGO_URI:", mongo_uri)

    if not mongo_uri or mongo_uri.startswith("="):
        print("❌ ERROR: MONGO_URI inválida o mal configurada")
        return None

    print("🔵 Probando conexión...")

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("🟢 Conexión exitosa a MongoDB")
        return client["ProyectoBonos"]

    except Exception as e:
        print("❌ Mongo ERROR:", e)
        return None

