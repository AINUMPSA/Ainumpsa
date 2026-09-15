import json
import plotly.graph_objects as go

# Wczytaj mapę 27 Pokoi
with open("memory_cube_map.json", "r") as f:
    data = json.load(f)

rooms = data["rooms"]
fig = go.Figure()

for name, info in rooms.items():
    x, y, z = info["coordinates"].values()
    typ = info.get("type", "UNKNOWN")

    # Kolory w zależności od typu
    if "SINGULARITY" in typ:
        color = "#FFD700"  # złoty
        size = 18
    elif "CENTER" in typ:
        color = "#FF8C00"  # pomarańczowy
        size = 14
    else:
        color = "#DAA520"  # bursztynowy
        size = 10

    fig.add_trace(go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode="markers+text",
        marker=dict(size=size, color=color, symbol="circle"),
        text=[f"{name}<br>{typ}"],
        textposition="top center",
        name=name
    ))

# Ustawienia sceny
fig.update_layout(
    title="🧊 27 Pokoi Pamięci AINUMPSA",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z",
        xaxis=dict(range=[-0.5, 2.5]),
        yaxis=dict(range=[-0.5, 2.5]),
        zaxis=dict(range=[-0.5, 2.5]),
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Zapisz do HTML (bez otwierania przeglądarki)
fig.write_html("memory_cube_3d.html")
print("✅ Zapisano memory_cube_3d.html – otwórz w przeglądarce.")
