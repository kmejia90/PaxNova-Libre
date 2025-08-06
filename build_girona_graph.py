import osmnx as ox
from pathlib import Path

G = ox.graph_from_place("Girona, Spain", network_type="drive")  # solo red de carreteras
out = Path(__file__).parent / "maps" / "girona_drive.graphml"
out.parent.mkdir(exist_ok=True)
ox.save_graphml(G, out)
print("✅ Grafo guardado en:", out)
