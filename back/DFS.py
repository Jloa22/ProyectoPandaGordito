import networkx as nx

def analizar_componentes(grafo, familias_dep):
    # Filtrar solo nodos que están en el grafo
    familias_dep = [f for f in familias_dep if f in grafo.nodes]

    # Obtener componentes conexos
    componentes = list(nx.connected_components(grafo))

    # Filtrar componentes que contengan familias del departamento
    componentes_dep = []
    for comp in componentes:
        comp_fams = [f for f in comp if f in familias_dep]
        if len(comp_fams) > 0:
            componentes_dep.append(comp_fams)

    # Ordenar por tamaño
    componentes_dep.sort(key=len, reverse=True)

    if len(componentes_dep) == 0:
        return {
            "componentes": [],
            "mayor_componente": 0,
            "segundo_componente": 0,
            "cantidad_componentes": 0,
            "porcentaje": 0
        }

    total = len(familias_dep)
    mayor = len(componentes_dep[0])
    segundo = len(componentes_dep[1]) if len(componentes_dep) > 1 else 0

    porcentaje = round((mayor / total) * 100, 2)

    return{
            "componentes": componentes_dep,
            "mayor_componente": mayor,
            "segundo_componente": segundo,
            "cantidad_componentes": len(componentes_dep),
            "porcentaje": porcentaje
    }
