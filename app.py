import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
# import the graph, coordinates and search algorithms from searchAlgos.py
from searchAlgos import (
    hospital_graph,
    locations,
    gbfs,
    a_star
)

# Streamlit GUI
#*******************#

st.set_page_config(page_title="Hospital Robot Search Visualizer", page_icon="🤖", layout="centered")

st.title("Emergency Supply Robot: Search Visualizer")
st.write(
    "Pick a start node, a goal node and a search algorithm (**GBFS** or **A\\***). "
    "The app runs the algorithm on the hospital corridor graph and highlights the solution path."
)

nodes = list(hospital_graph.keys())

start = st.selectbox("Select Initial Node", nodes, index=nodes.index("Pharmacy"))
goal = st.selectbox("Select Goal Node", nodes, index=nodes.index("Emergency_Ward"))
algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])

if st.button("Run Search"):

    if algorithm == "GBFS":
        path, cost, expansion_order = gbfs(start, goal)
    else:
        path, cost, expansion_order = a_star(start, goal)

    if path is None:
        st.error(f"No path found from {start} to {goal} (corridors are one-directional).")

    else:
        # Visualize NetworkX graph
        G = nx.DiGraph()
        for node, neighbors in hospital_graph.items():
            G.add_node(node)
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        pos = locations

        path_edges = list(zip(path, path[1:]))
        other_edges = [e for e in G.edges() if e not in path_edges]
        node_colors = [
            "#f28b82" if n == start else "#fdd663" if n == goal
            else "#a8dab5" if n in path else "#c6d4f0"
            for n in G.nodes()
        ]

        fig, ax = plt.subplots(figsize=(10, 6))

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1600, edgecolors="black", ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=other_edges, edge_color="gray", width=1.5,
                               arrowsize=18, node_size=1600, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=4,
                               arrowsize=22, node_size=1600, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"),
                                     font_size=9, label_pos=0.4, ax=ax)

        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")
        st.pyplot(fig)

        # Display result below the graph
        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")
        st.write(f"**Nodes Expanded (in order):** {' → '.join(expansion_order)}")
