import time
import networkx as nx
from back.datos import cargar_grafo

def es_entidad(n):
    return not n.isdigit()

def ejecutar_bellman_ford(familia_id: str):
    G = cargar_grafo()
    familia_id = familia_id.strip().upper()

    if familia_id not in G:
        return {"error": f"La familia {familia_id} no existe."}

    # Registrar tiempo
    inicio = time.time()

    # -----------------------------------------
    # 1️⃣ Obtener componente conexa (subgrafo)
    # -----------------------------------------
    componente = None
    for comp in nx.connected_components(G):
        if familia_id in comp:
            componente = comp
            break

    if componente is None:
        return {"error": "La familia no pertenece a un subgrafo conectado."}

    subG = G.subgraph(componente).copy()

    # -----------------------------------------
    # 2️⃣ Ejecutar Bellman–Ford sobre el subgrafo
    # -----------------------------------------
    try:
        distancias, rutas = nx.single_source_bellman_ford(
            subG, familia_id, weight="weight"
        )
    except nx.NetworkXUnbounded:
        return {"error": "El grafo contiene ciclos negativos."}

    # Obtener entidades alcanzables
    entidades = [n for n in subG.nodes() if es_entidad(n) and n in distancias]

    if not entidades:
        return {"error": "No existen entidades conectadas."}

    # Ordenar por menor costo
    entidades_ordenadas = sorted(
        [(e, distancias[e]) for e in entidades],
        key=lambda x: x[1]
    )[:3]

    fin = time.time()

    resultados = []
    for entidad, costo in entidades_ordenadas:
        ruta = rutas[entidad]
        bono_estimado = round(1 / costo, 2)
        resultados.append({
            "entidad": entidad,
            "ruta": ruta,
            "costo": costo,
            "bono_estimado": bono_estimado
        })

    # -----------------------------------------
    # 3️⃣ COMPLEJIDAD AUTOMÁTICA
    # -----------------------------------------
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
