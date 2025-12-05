from typing import Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from db.mongo_conn import get_db

# Inicializamos la BD y la colección
db = get_db()
users = db["users"]

# Alias de tipo para que Pylance sepa que un usuario es un diccionario
Usuario = Dict[str, Any]


def crear_usuario(nombre: str, correo: str, password: str) -> Dict[str, Any]:
    """
    Crea un usuario nuevo si el correo no existe.
    Retorna:
      - {"error": "..."} si ya existe
      - {"ok": True} si se registra correctamente
    """
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
    """
    Intenta loguear a un usuario.
    Retorna:
      - {"error": "..."} si algo falla
      - {"user": user_dict} si el login es correcto
    """
    user = users.find_one({"correo": correo})

    if not user:
        return {"error": "Correo no registrado"}

    # 👇 Cast explícito para que Pylance deje de decir que es "object"
    user = dict(user)  # type: ignore[arg-type]

    if not check_password_hash(user["password"], password):
        return {"error": "Contraseña incorrecta"}

    return {"user": user}
