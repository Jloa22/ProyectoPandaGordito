import pandas as pd
import networkx as nx

def cargar_grafo():
    # Leer CSV
    nodos = pd.read_csv("data/nodos.csv", dtype=str)
    aristas = pd.read_csv("data/aristas.csv", dtype=str)

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

    # --- AGREGAR ARISTAS SOLO FAMILIA → ENTIDAD ---
    aristas["Weight"] = pd.to_numeric(aristas["Weight"], errors="coerce").fillna(1.0)

    for _, row in aristas.iterrows():
        src, tgt = row["Source"], row["Target"]
        if src in G and tgt in G:
                peso = 1.0 / max(float(row["Weight"]), 1.0)
                G.add_edge(src, tgt, weight=peso)


    return G
