import os
from typing import Dict, List, Set
import pandas as pd
import networkx as nx

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RUTA_NODOS = os.path.join(ROOT_DIR, "data", "nodos.csv")

def ejecutar_dfs(grafo: nx.Graph, departamento: str) -> Dict[str, object]:
    dep = departamento.strip().upper()

    if not os.path.exists(RUTA_NODOS):
        return {
            "departamento": dep,
            "error": f"nodos.csv no encontrado en {RUTA_NODOS}",
            "cantidad": 0,
            "nodos_visitados": []
        }

    nodos = pd.read_csv(RUTA_NODOS)

    # Normalización
    nodos["Id"] = nodos["Id"].astype(str).str.strip().str.upper()
    nodos["Type"] = nodos["Type"].astype(str).str.lower()
    nodos["DEPARTAMENTO GRUPO FAMILIAR"] = (
        nodos["DEPARTAMENTO GRUPO FAMILIAR"]
        .astype(str).str.strip().str.upper()
    )

    # 1. 👉 Filtrar solo familias de ese departamento
    familias_dep: List[str] = nodos[
        (nodos["Type"] == "familia")
        & (nodos["DEPARTAMENTO GRUPO FAMILIAR"] == dep)
    ]["Id"].astype(str).tolist()

    if not familias_dep:
        return {
            "departamento": dep,
            "error": f"No hay familias registradas en {dep}.",
            "cantidad": 0,
            "nodos_visitados": []
        }

    # Asegurar que existan en el grafo
    familias_dep = [f for f in familias_dep if f in grafo.nodes]

    if not familias_dep:
        return {
            "departamento": dep,
            "error": f"Las familias del departamento {dep} no existen en el grafo.",
            "cantidad": 0,
            "nodos_visitados": []
        }

    visitados_set: Set[str] = set()

    # 2. 👉 Hacer DFS SOLO para familias de ese departamento
    for fam in familias_dep:
        for nodo in nx.dfs_preorder_nodes(grafo, source=fam):
            visitados_set.add(str(nodo))

    # 3. 👉 Filtrar SOLO familias del mismo departamento
    familias_conectadas = [
        f for f in visitados_set
        if f in familias_dep
    ]

    return {
        "departamento": dep,
        "cantidad": len(familias_conectadas),   # <= nunca supera las familias reales del departamento
        "nodos_visitados": familias_conectadas
    }
