from typing import Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from db.mongo_conn import get_db

# Inicializamos la BD y la colección
db = get_db()
if db is not None:
    users = db["users"]
else:
    print("❌ No hay DB, users no cargado")
    users = None


Usuario = Dict[str, Any]


def crear_usuario(nombre: str, correo: str, password: str) -> Dict[str, Any]:

    if users is None:
        return {"error": "Base de datos no disponible"}

    existente = users.find_one({"correo": correo})

    if existente:
        return {"error": "El correo ya está registrado"}

    user: Usuario = {
        "nombre": nombre,
        "correo": correo,
        "password": generate_password_hash(password)
    }

    users.insert_one(user)
    return {"ok": True}


def login_usuario(correo: str, password: str) -> Dict[str, Any]:

    if users is None:
        return {"error": "Base de datos no disponible"}

    user = users.find_one({"correo": correo})

    if not user:
        return {"error": "Correo no registrado"}

    user = dict(user)  # type: ignore[arg-type]

    if not check_password_hash(user["password"], password):
        return {"error": "Contraseña incorrecta"}

    return {"user": user}
