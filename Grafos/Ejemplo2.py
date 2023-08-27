#02/05/2023
#Fernando Patiño Reyes
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)

options = {
    "font_size": 36,
    "node_size": 3000,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 5,
    "width": 5,
}
# x,y
pos = {1: (0, 0), 2: (2, 0), 3: (4, 0),4:(6,0)}
nx.draw_networkx(G, pos, **options)

# Set margins for the axes so that nodes aren't clipped
ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()
