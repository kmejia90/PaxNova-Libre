"""
paxnova_maps.py – Módulo de mapas OFFLINE para Naomi
----------------------------------------------------
Requisitos instalados: osmnx, networkx, geopy, matplotlib
Grafo pre-generado: maps/girona_drive.graphml
"""

from pathlib import Path
import osmnx as ox
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────
# 1. Cargar grafo ligero (Girona) – se abre en 1-2 s
# ─────────────────────────────────────────────────────────────
GRAPH_FILE = Path(__file__).parent / "maps" / "girona_drive.graphml"
if not GRAPH_FILE.exists():
    raise FileNotFoundError(
        f"No se encontró {GRAPH_FILE}. Ejecuta build_girona_graph.py una vez."
    )

G = ox.load_graphml(GRAPH_FILE)

# ─────────────────────────────────────────────────────────────
# 2. Funciones públicas
# ─────────────────────────────────────────────────────────────
def buscar_coor(nombre: str):
    """
    Busca coordenadas en el grafo local (modo 100% offline).
    """
    nombre = nombre.strip().lower()
    for nodo_id, datos in G.nodes(data=True):
        if "name" in datos and datos["name"]:
            if nombre in datos["name"].lower():
                return (datos["y"], datos["x"])  # lat, lon
    return None


def distancia_recta(c1: tuple, c2: tuple) -> float:
    """Distancia geodésica en kilómetros entre dos (lat, lon)."""
    return geodesic(c1, c2).km


def ruta_en_coche(c1: tuple, c2: tuple):
    """
    Devuelve:
      • lista de nodos de la ruta más corta (por longitud)
      • distancia en km
    """
    n1 = ox.nearest_nodes(G, c1[1], c1[0])  # lon, lat
    n2 = ox.nearest_nodes(G, c2[1], c2[0])
    ruta = nx.shortest_path(G, n1, n2, weight="length")
    dist_km = nx.path_weight(G, ruta, weight="length") / 1000
    return ruta, dist_km

def describir_ruta(ruta: list, umbral_m: int = 50, max_pasos: int = 12) -> str:
    """
    Crea instrucciones simplificadas agrupando tramos consecutivos con el mismo nombre.
    - umbral_m: ignora segmentos menores (ruido)
    """
    pasos = []
    calle_actual = None
    acum = 0.0

    for u, v in zip(ruta[:-1], ruta[1:]):
        datos = G.get_edge_data(u, v)[0]
        nombre = datos.get("name", "vía sin nombre")
        longitud = datos["length"]  # en metros

        if nombre == calle_actual:
            acum += longitud
        else:
            # Guarda el paso anterior
            if calle_actual and acum > umbral_m:
                pasos.append(f"• Sigue por {calle_actual} durante {acum/1000:.1f} km")
            # Reinicia
            calle_actual = nombre
            acum = longitud

        if len(pasos) >= max_pasos:
            break

    # Último tramo
    if calle_actual and acum > umbral_m and len(pasos) < max_pasos:
        pasos.append(f"• Continúa por {calle_actual} los últimos {acum/1000:.1f} km")

    return "\n".join(pasos) if pasos else "Ruta demasiado corta para detallar pasos."



def guardar_mapa(ruta: list, nombre_png: str = "maps/ultima_ruta.png"):
    """
    Dibuja el grafo y destaca la ruta en rojo.
    Guarda el resultado como PNG y devuelve la ruta del archivo.
    """
    fig, ax = ox.plot_graph_route(
        G,
        ruta,
        route_color="red",
        route_linewidth=3,
        bgcolor="white",
        node_size=0,
        show=False,
        close=False,
    )
    nombre_png = Path(nombre_png)
    nombre_png.parent.mkdir(exist_ok=True, parents=True)
    fig.savefig(nombre_png, dpi=150)
    plt.close(fig)
    return str(nombre_png)
