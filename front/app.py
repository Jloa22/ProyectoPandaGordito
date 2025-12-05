# ========================================
#  AJUSTE DE RUTA PARA IMPORTAR /back
# ========================================
import sys
import os
from typing import Any, Dict, cast

# ========================================
#  AJUSTE DE RUTA PARA IMPORTAR /db
# ========================================
import sys as _sys2  # solo para que no moleste el linter
import os as _os2

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from db.logs_db import guardar_log

# ========================================
#            IMPORTS NORMALES
# ========================================
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import streamlit.components.v1 as components

from back.dijkstra import ejecutar_dijkstra
from back.DFS import ejecutar_dfs
from back.datos import cargar_grafo
from db.users_db import crear_usuario, login_usuario

# ----------------------------
#  CONFIGURACIÓN DE PÁGINA
# ----------------------------
st.set_page_config(
    page_title="Plataforma CUPO X VIVIENDA",
    page_icon="🏠",
    layout="wide"
)

# ----------------------------
#        ESTILOS CACHINEROS
# ----------------------------
st.markdown(
    """
<style>

    :root {
        --bg-main: #f3f4f6;
        --bg-card: #ffffff;
        --bg-card-soft: #f9fafb;
        --border-soft: #d1d5db;
        --accent: #2563eb;
        --accent-soft: rgba(37, 99, 235, 0.15);
        --accent-alt: #1d4ed8;
        --text-main: #111827;
        --text-muted: #6b7280;
        --text-soft: #9ca3af;
    }

    .stApp {
        background: linear-gradient(180deg, #ffffff 0%, #eef2ff 100%);
        color: var(--text-main);
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    section[data-testid="stSidebar"] {
        background: #1e3a8a !important;
        color: white !important;
        border-right: 1px solid #1e40af;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .big-title {
        font-size: 38px !important;
        color: #1e3a8a;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        font-size: 15px;
        color: var(--text-muted);
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.25rem;
    }

    .section-subtitle {
        font-size: 13px;
        color: var(--text-soft);
        margin-bottom: 0.8rem;
    }

    .card {
        background: var(--bg-card);
        padding: 18px 20px;
        border-radius: 16px;
        border: 1px solid var(--border-soft);
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        margin-bottom: 18px;
    }

    .card-soft {
        background: var(--bg-card-soft);
        padding: 14px 16px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        margin-bottom: 16px;
    }

    .pill {
        display: inline-flex;
        padding: 4px 10px;
        border-radius: 999px;
        background: var(--accent-soft);
        color: var(--accent);
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 0.7rem;
    }

    .metric-label {
        font-size: 11px;
        color: var(--text-soft);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 600;
    }

    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #1e3a8a;
    }

    .metric-badge {
        font-size: 11px;
        color: var(--accent);
        background: var(--accent-soft);
        padding: 2px 9px;
        border-radius: 999px;
        margin-top: 4px;
    }

    .tag {
        display: inline-flex;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 11px;
        margin-right: 4px;
        margin-top: 4px;
        border: 1px solid var(--border-soft);
    }
    .tag-blue {
        background: rgba(37, 99, 235, 0.15);
        color: #1d4ed8;
    }

    .tag-emerald {
        background: rgba(16,185,129,0.15);
        color: #059669;
    }

    .tag-amber {
        background: rgba(245,158,11,0.15);
        color: #d97706;
    }

    .algo-title {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .algo-desc {
        font-size: 13px;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
    }

    .footer-note {
        font-size: 12px;
        color: var(--text-soft);
        margin-top: 1.5rem;
    }

    button[kind="primary"] {
        border-radius: 999px !important;
        font-weight: 600 !important;
        background: var(--accent) !important;
        color: white !important;
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background-color: white !important;
        border-radius: 999px !important;
        border: 1px solid var(--border-soft) !important;
        color: var(--text-main) !important;
    }

</style>
""",
    unsafe_allow_html=True,
)

st.markdown("""
<style>

    /* ==============================
       🔧 FIX: INPUTS (login/registro)
       ============================== */
    input, 
    .stTextInput > div > div > input {
        color: black !important;
        background: white !important;
    }

    /* Placeholder negro */
    input::placeholder {
        color: black !important;
        opacity: 1 !important;
    }

    /* Labels */
    label, .stTextInput label {
        color: black !important;
        font-weight: 600 !important;
    }

    /* ==============================
       🔧 FIX: SELECTBOX
       ============================== */
    .stSelectbox div[data-baseweb="select"] * {
        color: black !important;   /* Texto interno */
    }

    div[role="listbox"] div[data-testid="styled-option"] {
        color: black !important; 
        background: white !important;
    }

    /* ==============================
       🔧 FIX: BOTONES (volver a blanco)
       ============================== */
    div.stButton > button {
        color: white !important;          /* Texto blanco visible */
        background-color: #2563eb !important; /* Azul original */
        border-radius: 999px !important;
        font-weight: 600 !important;
    }

    /* Hover más oscuro */
    div.stButton > button:hover {
        background-color: #1e40af !important;
        color: white !important;
    }

</style>
""", unsafe_allow_html=True)



@st.cache_data
def cargar_datos():
    nodos = pd.read_csv("data/nodos.csv", dtype=str)
    aristas = pd.read_csv("data/aristas.csv", dtype=str, low_memory=False)

    nodos["Id"] = nodos["Id"].str.strip().str.upper()
    nodos["Type"] = nodos["Type"].str.strip().str.lower()
    nodos["DEPARTAMENTO GRUPO FAMILIAR"] = (
        nodos["DEPARTAMENTO GRUPO FAMILIAR"].str.strip().str.upper()
    )
    return nodos, aristas


# ----------------------------
#       LOGIN / REGISTRO MONGO
# ----------------------------

session_state = cast(Dict[str, Any], st.session_state)

if "usuario" not in session_state:
    session_state["usuario"] = None

if session_state["usuario"] is None:

    st.title("🔐 Iniciar Sesión")

    tab_login, tab_registro = st.tabs(["Iniciar Sesión", "Registrarse"])

    # LOGIN
    with tab_login:
        correo = st.text_input("Correo")
        password = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            r = login_usuario(correo, password)
            if "error" in r:
                st.error(r["error"])
            else:
                session_state["usuario"] = r["user"]
                st.success(f"Bienvenido {r['user']['nombre']}")
                st.rerun()

    # REGISTRO
    with tab_registro:
        nombre = st.text_input("Nombre completo")
        correo_r = st.text_input("Correo nuevo")
        pw_r = st.text_input("Contraseña nueva", type="password")

        if st.button("Crear cuenta"):
            r = crear_usuario(nombre, correo_r, pw_r)
            if "error" in r:
                st.error(r["error"])
            else:
                st.success("Usuario registrado correctamente")

    st.stop()



# ----------------------------
#       MENÚ LATERAL
# ----------------------------
st.sidebar.markdown("### 🏠 BonoVivienda")
st.sidebar.markdown(
    "<small>Sistema de análisis de familias, entidades y comunidades usando algoritmos de grafos.</small>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

opcion = st.sidebar.radio(
    "Navegación:",
    ["🏠 Inicio", "▶️ Recomendar entidad", "🕸️ Grafo por departamento"],
)
# -----------------------------------
# BOTÓN DE CERRAR SESIÓN (ABAJO)
# -----------------------------------

st.sidebar.markdown("""
<br><br><br><br><br>
<div style='position: absolute; bottom: 20px; width: 90%;'>
""", unsafe_allow_html=True)

if session_state["usuario"] is not None:
    if st.sidebar.button("🔓 Cerrar sesión"):
        session_state["usuario"] = None
        st.rerun()

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# =====================================================
#                      HOME
# =====================================================
if opcion == "🏠 Inicio":
    st.markdown(
        """
        <div>
            <div class="pill">Plataforma académica · Estructura de Datos</div>
            <p class='big-title'>🏠 Plataforma BonoVivienda</p>
            <p class="subtitle">
                Visualiza y analiza la relación entre <b>familias beneficiarias</b>, 
                <b>entidades técnicas</b> y sus <b>comunidades</b> usando algoritmos de grafos
                como Dijkstra, Bellman-Ford y DFS.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nodos, aristas = cargar_datos()
    familias_df = nodos[nodos["Type"] == "familia"]
    entidades_df = nodos[nodos["Type"] == "entidad"]
    comunidades_info: Dict[str, Any] = {"total": 0}

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                '<div class="metric-label">Familias</div>', unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="metric-value">{len(familias_df):,}</div>'.replace(
                    ",", "."
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                '<span class="metric-badge">Nodos tipo familia</span>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                '<div class="metric-label">Entidades técnicas</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="metric-value">{len(entidades_df):,}</div>'.replace(
                    ",", "."
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                '<span class="metric-badge">Nodos tipo entidad</span>',
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                '<div class="metric-label">Conexiones</div>', unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="metric-value">{len(aristas):,}</div>'.replace(",", "."),
                unsafe_allow_html=True,
            )
            st.markdown(
                '<span class="metric-badge">Aristas familia–entidad</span>',
                unsafe_allow_html=True,
            )


    st.markdown("")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<div class='algo-title'>🔍 Dijkstra</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='algo-desc'>Calcula la ruta óptima entre una familia y las entidades técnicas, "
            "recomendando la mejor entidad según el peso del bono.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<span class="tag tag-blue">Ruta mínima</span>'
            '<span class="tag tag-emerald">Recomendación</span>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<div class='algo-title'>🧩 Bellman–Ford</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='algo-desc'>Algoritmo capaz de calcular rutas óptimas incluso en grafos con pesos negativos. "
            "Permite comparar su rendimiento con Dijkstra en la recomendación de entidades técnicas.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(    
        '<span class="tag tag-amber">Ruta óptima</span>'
        '<span class="tag tag-blue">Comparación de eficiencia</span>',
        unsafe_allow_html=True,
    )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<div class='algo-title'>🌍 DFS</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='algo-desc'>Explora la conectividad de las familias por departamento, "
            "mostrando cuántas están conectadas dentro de la red.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<span class="tag tag-amber">Recorrido en profundidad</span>'
            '<span class="tag tag-blue">Cobertura</span>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)



    st.markdown(
        "<div class='footer-note'>Proyecto académico de análisis de grafos aplicado al Bono Familiar Habitacional.</div>",
        unsafe_allow_html=True,
    )
# Inicializar variables para evitar errores
    ver_final = False
    buscar = False
    ver_detalles = False

# =====================================================
#                     DIJKSTRA
# =====================================================
elif opcion == "▶️ Recomendar entidad":

    st.markdown("""
        <div class="pill">Módulo de recomendación</div>
        <p class='big-title'>🔍 Dijkstra: entidad técnica recomendada</p>
        <p class="subtitle">
            Selecciona un <b>departamento</b> y una <b>familia</b> para obtener 
            las 3 mejores entidades técnicas y visualizar el grafo.
        </p>
    """, unsafe_allow_html=True)

    nodos, aristas = cargar_datos()
    familias_df = nodos[nodos["Type"] == "familia"]
    departamentos = sorted(familias_df["DEPARTAMENTO GRUPO FAMILIAR"].dropna().unique())

    familia = None

    # =======================
    #   FILTROS INICIALES
    # =======================
    col_filtros, col_info = st.columns([2, 1.2])
    with col_filtros:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        dep = st.selectbox("🏙️ Filtra por departamento", departamentos)

        familias_dep = sorted(
            familias_df[familias_df["DEPARTAMENTO GRUPO FAMILIAR"] == dep]["Id"].unique()
        )

        if familias_dep:
            familia = st.selectbox("👨‍👩‍👧‍👦 Seleccione una familia", familias_dep)
            buscar = st.button("🔎 Buscar entidad recomendada", use_container_width=True)
        else:
            st.warning("No hay familias disponibles en este departamento.")
            buscar = False

        st.markdown("</div>", unsafe_allow_html=True)

    with col_info:
        st.markdown('<div class="card-soft">', unsafe_allow_html=True)
        st.markdown("<div class='section-title'>¿Qué hace este módulo?</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class="section-subtitle">
            • Muestra el grafo inicial.<br>
            • Recomienda la mejor entidad.<br>
            • Permite comparar Bellman–Ford vs Dijkstra.<br>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ===================================================
    #               RESULTADO + GRAFO INICIAL
    # ===================================================
    if buscar:

        if not familia:
            st.error("Debe seleccionar una familia.")
            st.stop()

        G = cargar_grafo()
        conexiones_directas = list(G.neighbors(familia))
        subG = G.subgraph([familia] + conexiones_directas)

        resultado = ejecutar_dijkstra(familia, top_n=3)
        st.session_state["resultado_dijkstra"] = resultado

        # 📌 Diseño: 2 columnas → Izquierda grafo / Derecha top resultados
        col_grafo, col_resumen = st.columns([2, 1])

        # -------------------------------
        #     GRAFO INICIAL
        # -------------------------------
        with col_grafo:
            st.markdown("### 📊 Grafo inicial")
            grafo_inicial = Network(height="700px", width="100%", bgcolor="#ffffff")
            grafo_inicial.set_options("""{
            "physics": { "enabled": true },
            "nodes": { "font": { "size": 18 } }
            }""")

            grafo_inicial.add_node(familia, color="#2563eb", size=40, title="FAMILIA")

            for n in conexiones_directas:
                grafo_inicial.add_node(n, color="#10b981", size=30, title="ENTIDAD")

            for u, v, data in subG.edges(data=True):
                grafo_inicial.add_edge(u, v, title=f"Peso: {data.get('weight', 1):.4f}")

            grafo_inicial.save_graph("grafo_inicial.html")
            components.html(open("grafo_inicial.html", "r", encoding="utf-8").read(),
                            height=700)

        # -------------------------------
        #     TOP 3 ENTIDADES
        # -------------------------------
        with col_resumen:
            st.markdown("### 🏆 Mejores entidades")
            if resultado.get("mejores_opciones"):
                mejor = resultado["mejores_opciones"][0]
                st.session_state["ruta_final"] = mejor["ruta"]
                st.session_state["bono_final"] = mejor["bono_estimado"]

                for idx, op in enumerate(resultado["mejores_opciones"], start=1):
                    st.markdown(f"**🔹 Opción {idx}: {op['entidad']}**")
                    st.write(f"Ruta: {' → '.join(op['ruta'])}")
                    st.write(f"Bono: **{op['bono_estimado']}**")
                    st.markdown("---")

                st.button("🚀 Ver grafo final", key="btn_ver_final")

            else:
                st.error("No hay entidades conectadas.")

    # ===================================================
    #                   GRAFO FINAL + COMPARACIÓN
    # ===================================================
    if st.session_state.get("btn_ver_final") and "ruta_final" in st.session_state:

        ruta_final = st.session_state["ruta_final"]
        bono = st.session_state["bono_final"]

        col_grafo_final, col_comp = st.columns([2, 1])

        # -------------------------------
        #     GRAFO FINAL
        # -------------------------------
        with col_grafo_final:
            st.markdown("### 🚀 Grafo Final - Ruta óptima")

            grafo_final = Network(height="700px", width="100%", bgcolor="#ffffff")
            grafo_final.set_options("""{
            "physics": { "enabled": false },
            "nodes": { "font": { "size": 20 } }
            }""")

            for i, nodo in enumerate(ruta_final):
                if i == 0:
                    grafo_final.add_node(nodo, color="#2563eb", size=45)
                elif i == len(ruta_final) - 1:
                    grafo_final.add_node(
                        nodo, color="#dc2626", size=50,
                        title=f"Bono {bono:.2f}"
                    )
                else:
                    grafo_final.add_node(nodo, color="#10b981", size=35)

            for i in range(len(ruta_final) - 1):
                grafo_final.add_edge(ruta_final[i], ruta_final[i+1], color="red")

            grafo_final.save_graph("grafo_final.html")
            components.html(open("grafo_final.html", "r", encoding="utf-8").read(),
                            height=700)

        # -------------------------------
        #     COMPARACIÓN BF vs DIJKSTRA
        # -------------------------------
        with col_comp:

            st.markdown("### 🏆 Entidad recomendada:")
            mejor_entidad= st.session_state["ruta_final"][-1] 
            st.markdown(f"### ⭐ {mejor_entidad}")     
            st.markdown("---")      
            st.markdown("### ⚡ Comparación de rendimiento")
            
            from back.bellman_ford import ejecutar_bellman_ford
            res_bell = ejecutar_bellman_ford(ruta_final[0])

            op_d = st.session_state["resultado_dijkstra"]["mejores_opciones"][0]
            tiempo_d = st.session_state["resultado_dijkstra"]["tiempo"]

            op_b = res_bell["mejores_opciones"][0]
            tiempo_b = res_bell["tiempo"]

            st.markdown("#### 🟦 Dijkstra")
            st.write(f"Ruta: {' → '.join(op_d['ruta'])}")
            st.write(f"Tiempo: **{tiempo_d}s**")
            st.write(f"Bono: {op_d['bono_estimado']}")
            st.write(f"Complejidad: **{st.session_state['resultado_dijkstra']['complejidad']}**")

            st.markdown("#### 🟥 Bellman-Ford")
            st.write(f"Ruta: {' → '.join(op_b['ruta'])}")
            st.write(f"Tiempo: **{tiempo_b}s**")
            st.write(f"Bono: {op_b['bono_estimado']}")
            st.write(f"Complejidad: {res_bell['complejidad']}")


            st.info("💡 Dijkstra suele ser más eficiente en grafos sin pesos negativos.")


# =====================================================
#             GRAFO POR DEPARTAMENTO (NUEVO)
# =====================================================
elif opcion == "🕸️ Grafo por departamento":

    st.markdown(
        """
        <div class="pill">Visualización estructural</div>
        <p class='big-title'>🕸️ Grafo por departamento</p>
        <p class="subtitle">
            Genera el subgrafo formado por las <b>familias</b> de un departamento y las <b>entidades</b> 
            conectadas a ellas. Se muestran el número de <b>nodos</b> y <b>aristas</b> asociados al departamento.
        </p>
        """,
        unsafe_allow_html=True,
    )

    nodos, aristas = cargar_datos()
    G = cargar_grafo()

    familias_df = nodos[nodos["Type"] == "familia"].copy()
    entidades_df = nodos[nodos["Type"] == "entidad"].copy()

    departamentos = sorted(
        familias_df["DEPARTAMENTO GRUPO FAMILIAR"].dropna().unique()
    )

    # Mapa Id -> Type para colorear nodos
    tipo_por_id: Dict[str, str] = nodos.set_index("Id")["Type"].to_dict()

    col_sel, col_info = st.columns([1.6, 2.0])

    with col_sel:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        dep = st.selectbox(
            "🏙️ Seleccione departamento", departamentos, key="dep_grafo"
        )
        generar = st.button(
            "🕸️ Generar grafo del departamento", use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_info:
        st.markdown('<div class="card-soft">', unsafe_allow_html=True)
        st.markdown(
            "<div class='section-title'>¿Qué representa este grafo?</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="section-subtitle">
            • Incluye todas las <b>familias</b> del departamento seleccionado.<br>
            • Agrega las <b>entidades técnicas</b> conectadas a esas familias.<br>
            • Se cuentan las <b>aristas</b> que enlazan familias con entidades.<br>
            • Permite comparar departamentos por su nivel de conexión (número de aristas).<br>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if generar:
        if dep is None or dep == "":
            st.error("Debe seleccionar un departamento.")
            st.stop()

        dep_str = cast(str, dep)
        st.markdown(
            f"<p class='section-title'>Subgrafo asociado a {dep_str}</p>",
            unsafe_allow_html=True,
        )

        # Familias del departamento
        familias_dep = familias_df[
            familias_df["DEPARTAMENTO GRUPO FAMILIAR"] == dep_str
        ]["Id"].tolist()

        if not familias_dep:
            st.warning("No hay familias registradas para este departamento.")
            st.stop()

        # Construir conjunto de nodos relevantes:
        # familias del departamento + entidades conectadas
        nodos_dep = set()
        entidades_conectadas = set()

        for fam in familias_dep:
            if fam in G:
                nodos_dep.add(fam)
                for vecino in G.neighbors(fam):
                    nodos_dep.add(vecino)
                    if tipo_por_id.get(vecino, "") == "entidad":
                        entidades_conectadas.add(vecino)

        if not nodos_dep:
            st.warning(
                "No se encontraron conexiones en el grafo para este departamento."
            )
            st.stop()

        subG = G.subgraph(nodos_dep).copy()

        num_nodos = subG.number_of_nodes()
        num_aristas = subG.number_of_edges()

        # Contar familias y entidades del subgrafo
        familias_en_subgrafo = [
            n for n in subG.nodes if tipo_por_id.get(n, "") == "familia"
        ]
        entidades_en_subgrafo = [
            n for n in subG.nodes if tipo_por_id.get(n, "") == "entidad"
        ]

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(
                '<div class="metric-label">Nodos totales</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="metric-value">{num_nodos}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<span class="metric-badge">Familias + entidades</span>',
                unsafe_allow_html=True,
            )
        with col_m2:
            st.markdown(
                '<div class="metric-label">Aristas</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="metric-value">{num_aristas}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<span class="metric-badge">Conexiones en el subgrafo</span>',
                unsafe_allow_html=True,
            )
        with col_m3:
            st.markdown(
                '<div class="metric-label">Distribución</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="metric-value">{len(familias_en_subgrafo)}/{len(entidades_en_subgrafo)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<span class="metric-badge">Familias / Entidades</span>',
                unsafe_allow_html=True,
            )

        # Resumen numérico
        resumen_df = pd.DataFrame(
            {
                "Departamento": [dep_str],
                "Nodos_totales": [num_nodos],
                "Familias": [len(familias_en_subgrafo)],
                "Entidades": [len(entidades_en_subgrafo)],
                "Aristas": [num_aristas],
            }
        )
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(
            "<p class='section-title'>Resumen numérico del subgrafo</p>",
            unsafe_allow_html=True,
        )
        st.dataframe(resumen_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Grafo interactivo con PyVis
        st.markdown("### 🌐 Visualización del grafo")

        grafo_dep = Network(
            height="700px",
            width="1000px",
            bgcolor="#ffffff",
            directed=False,
        )

        grafo_dep.set_options(
            """
        var options = {
        "physics": {
            "enabled": true,
            "barnesHut": {
            "gravitationalConstant": -3500,
            "centralGravity": 0.4,
            "springLength": 200,
            "springConstant": 0.04,
            "damping": 0.09
            }
        },
        "nodes": {
            "font": { "size": 18, "face": "arial" }
        }
        }
        """
        )

        # Añadir nodos con color según tipo
        for n in subG.nodes():
            tipo = tipo_por_id.get(n, "")
            if tipo == "familia":
                grafo_dep.add_node(
                    n, color="#2563eb", size=35, title=f"Familia {n}"
                )
            elif tipo == "entidad":
                grafo_dep.add_node(
                    n, color="#10b981", size=30, title=f"Entidad {n}"
                )
            else:
                grafo_dep.add_node(
                    n, color="#6b7280", size=25, title=str(n)
                )

        # Añadir aristas
        for u, v, data in subG.edges(data=True):
            peso = data.get("weight", 1)
            grafo_dep.add_edge(u, v, title=f"Peso: {peso}")

        path_html_dep = "grafo_departamento.html"
        grafo_dep.save_graph(path_html_dep)


        # ============================================================
        #   🔍 ANALÍTICA: GRAFO + RESUMEN LADO A LADO
        # ============================================================

        # Crear columnas: grafo a la izquierda, stats a la derecha
        col_grafo_dep, col_stats_dep = st.columns([2, 1])

        # -------------------------
        #  GRAFO EN LA COLUMNA IZQ
        # -------------------------
        with col_grafo_dep:
            components.html(
                open(path_html_dep, "r", encoding="utf-8").read(),
                height=700,
                width=900,
                scrolling=True,
            )

        # -------------------------
        #  ESTADÍSTICAS A LA DERECHA
        # -------------------------
        with col_stats_dep:
            st.markdown("### 📌 Resumen del departamento seleccionado")

            # Conteo global de familias por departamento
            conteo_fam = familias_df["DEPARTAMENTO GRUPO FAMILIAR"].value_counts()

            # Total de familias del departamento seleccionado
            total_dep = int(conteo_fam.get(dep_str, 0))

            # Crear ranking ordenado (nombre correcto de columnas)
            ranking = (
                conteo_fam
                .sort_values(ascending=False)
                .reset_index()
            )
            # Aquí forzamos nombres claros, sin adivinar
            ranking.columns = ["Departamento", "Familias"]

            # Buscar la fila del departamento seleccionado
            pos_row = ranking[ranking["Departamento"] == dep_str]

            if len(pos_row) > 0:
                pos = int(pos_row.index[0] + 1)
            else:
                pos = "-"

            # Texto principal
            st.markdown(f"""
            **Departamento:** 🔵 **{dep_str}**  
            • Familias conectadas: **{total_dep}**  
            • Ranking nacional: **#{pos}**
            """)

            # TOP 5 DEPARTAMENTOS
            st.markdown("### 🥇 Mayor número de familias")
            top5 = conteo_fam.sort_values(ascending=False).head(5)
            for dep_nombre, num in top5.items():
                st.markdown(f"**{dep_nombre}** → {num} familias")

            # BOTTOM 5 DEPARTAMENTOS
            st.markdown("### ⚠️ Menor cobertura (menos familias conectadas)")
            low5 = conteo_fam.sort_values().head(5)
            for dep_nombre, num in low5.items():
                st.markdown(f"**{dep_nombre}** → {num} familias")

