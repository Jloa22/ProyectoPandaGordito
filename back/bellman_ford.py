import time
import networkx as nx
from back.datos import cargar_grafo


# -----------------------------
#  DETECTOR CORRECTO DE ENTIDAD
# -----------------------------
def es_entidad(n, G):
    return G.nodes[n].get("tipo") == "entidad"


def ejecutar_bellman_ford(familia_id: str):
    G = cargar_grafo()
    familia_id = familia_id.strip().upper()

    if familia_id not in G:
        return {"error": f"La familia {familia_id} no existe."}

    inicio = time.time()

    # ---------------------------------------
    #  Encontrar componente conexa
    # ---------------------------------------
    componente = None
    for comp in nx.connected_components(G):
        if familia_id in comp:
            componente = comp
            break

    if componente is None:
        return {"error": "La familia no pertenece a un subgrafo conectado."}

    subG = G.subgraph(componente).copy()

    # ---------------------------------------
    #  Entidades reales (usando atributo tipo)
    # ---------------------------------------
    entidades = [n for n in subG.nodes() if es_entidad(n, subG)]

    if not entidades:
        return {"error": "No existen entidades conectadas."}

    # ---------------------------------------
    #  Ejecutar Bellman-Ford
    # ---------------------------------------
    try:
        distancias, rutas = nx.single_source_bellman_ford(
            subG, familia_id, weight="weight"
        )
    except nx.NetworkXUnbounded:
        return {"error": "El grafo contiene ciclos negativos."}

    entidades_dist = [(e, distancias[e]) for e in entidades if e in distancias]

    mejores = sorted(entidades_dist, key=lambda x: x[1])[:3]

    resultados = []
    for entidad, costo in mejores:
        ruta = rutas[entidad]
        bono_estimado = round(1 / costo, 2)
        resultados.append({
            "entidad": entidad,
            "ruta": ruta,
            "costo": costo,
            "bono_estimado": bono_estimado
        })

    fin = time.time()

    # Complejidad
    V = subG.number_of_nodes()
    E = subG.number_of_edges()

    complejidad = f"O(V·E) = O({V} × {E})"

    return {
        "familia": familia_id,
        "mejores_opciones": resultados,
        "tiempo": round(fin - inicio, 6),
        "V": V,
        "E": E,
        "complejidad": complejidad
    }
