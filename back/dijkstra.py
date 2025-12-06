import time
import networkx as nx
from back.datos import cargar_grafo


# -----------------------------
#  DETECTOR CORRECTO DE ENTIDAD
# -----------------------------
def es_entidad(n, G):
    return G.nodes[n].get("tipo") == "entidad"


def ejecutar_dijkstra(familia_id: str, top_n: int = 3):
    G = cargar_grafo()
    familia_id = familia_id.strip().upper()

    if familia_id not in G:
        return {"error": f"La familia {familia_id} no existe en el grafo."}

    # Tiempo de inicio
    inicio = time.time()

    # ---------------------------------
    #  Obtener componente conexa
    # ---------------------------------
    componente = None
    for comp in nx.connected_components(G):
        if familia_id in comp:
            componente = comp
            break

    if componente is None:
        return {"error": "La familia no está en un subgrafo conectado."}

    subG = G.subgraph(componente).copy()

    # ---------------------------------
    #   Identificar entidades reales
    # ---------------------------------
    entidades = [n for n in subG.nodes() if es_entidad(n, subG)]

    if not entidades:
        return {"error": "No hay entidades conectadas."}

    # ---------------------------------
    #  Ejecutar Dijkstra
    # ---------------------------------
    distancias = nx.single_source_dijkstra_path_length(
        subG, familia_id, weight="weight"
    )

    entidades_dist = [(e, distancias[e]) for e in entidades if e in distancias]

    if not entidades_dist:
        return {"error": "No existen rutas desde esta familia a entidades."}

    mejores = sorted(entidades_dist, key=lambda x: x[1])[:top_n]

    resultados = []
    for entidad, costo in mejores:
        ruta = nx.dijkstra_path(subG, familia_id, entidad, weight="weight")
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

    complejidad = f"O(E log V) = O({E} log {V})"

    return {
        "familia": familia_id,
        "mejores_opciones": resultados,
        "tiempo": round(fin - inicio, 6),
        "complejidad": complejidad,
        "V": V,
        "E": E
    }
