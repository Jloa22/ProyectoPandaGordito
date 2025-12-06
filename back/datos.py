import os
import pandas as pd
import networkx as nx

# BASE_DIR = carpeta raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
DATA_DIR = os.path.join(BASE_DIR, "data")

def cargar_grafo():

    # Leer CSV con ruta absoluta (funciona en PC y Railway)
    nodos = pd.read_csv(os.path.join(DATA_DIR, "nodos.csv"), dtype=str)
    aristas = pd.read_csv(os.path.join(DATA_DIR, "aristas.csv"), dtype=str)

    G = nx.Graph()

    # --- AGREGAR NODOS ---
    for _, row in nodos.iterrows():
        G.add_node(
            row["Id"],
            tipo=row["Type"],
            departamento=row.get("DEPARTAMENTO GRUPO FAMILIAR"),
            distrito=row.get("DISTRITO GRUPO FAMILIAR"),
            modalidad=row.get("MODALIDAD"),
        )

    # --- AGREGAR ARISTAS ---
    aristas["Weight"] = pd.to_numeric(aristas["Weight"], errors="coerce").fillna(1.0)

    for _, row in aristas.iterrows():
        src, tgt = row["Source"], row["Target"]
        if src in G and tgt in G:
            peso = 1.0 / max(float(row["Weight"]), 1.0)
            G.add_edge(src, tgt, weight=peso)

    return G
