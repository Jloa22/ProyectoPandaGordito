print("🔵 Railway detecta mongo_conn.py iniciando...")
import os
import streamlit as st
from pymongo import MongoClient

def get_db():
    try:
        mongo_uri = st.secrets.get("MONGO_URI", None)
    except:
        mongo_uri = None

    if not mongo_uri:
        mongo_uri = os.getenv("MONGO_URI")

    print("🔵 Cargando MONGO_URI:", mongo_uri)

    if not mongo_uri:
        print("❌ No se encontró MONGO_URI en Railway")
        return None

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("🟢 Conexión exitosa a MongoDB")
        return client["ProyectoBonos"]
    except Exception as e:
        print("❌ Mongo ERROR:", e)
        return None

