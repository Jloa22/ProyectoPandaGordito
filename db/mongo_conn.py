import os
import streamlit as st
from pymongo import MongoClient

def get_db():
    # Primero intenta leer desde streamlit secrets (local)
    try:
        mongo_uri = st.secrets["MONGO_URI"]
    except:
        # Si no está en Streamlit, lo busca en variable de entorno (Railway)
        mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise ValueError("❌ ERROR: No se encontró la variable de entorno MONGO_URI")

    client = MongoClient(mongo_uri)
    return client["ProyectoBonos"]
