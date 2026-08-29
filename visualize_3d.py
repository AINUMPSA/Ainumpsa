import json
import plotly.graph_objects as go

with open("memory_cube_map.json", "r") as f:
    data = json.load(f)

rooms = data["rooms"]
fig = go.Figure()

for name, info in rooms.items():
    x, y, z = info["coordinates"].values()
    color = "gold" if "SINGULARITY" in info["type"] else "orange" if "CENTER" in info["type"] else "gray"
    fig.add_trace(go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode="markers+text",
        marker=dict(size=10, color=color),
        text=[name],
        textposition="top center"
    ))

fig.update_layout(scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"))
fig.show()
