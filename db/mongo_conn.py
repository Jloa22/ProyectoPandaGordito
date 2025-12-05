import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ ERROR: No se encontró la variable de entorno MONGO_URI")

client = MongoClient(MONGO_URI)

def get_db():
    return client["ProyectoBonos"]
