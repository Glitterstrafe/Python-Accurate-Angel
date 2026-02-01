import networkx as nx
from pyvis.network import Network
from typing import List
from .types import AngelEvent, EdgeDef


class Sephirot:
    """
    The Graph Visualizer.
    Now with 100% more Glow and Cyber-Aesthetics.
    """
    def __init__(self):
        self.graph = nx.DiGraph()

        # --- THE PALETTE ---
        self.c_file = "#FFD700"   # Gold (Matter)
        self.c_intent = "#FF69B4" # Hot Pink (Spirit)
        self.c_edge = "rgba(255, 255, 255, 0.6)" # Translucent White

    def clear(self):
        self.graph.clear()

    def rebuild_from_chronicles(self, events: List[AngelEvent]):
        """Replays history to build current state."""
        self.graph.clear()
        for event in events:
            if event.action_type == "PROPOSAL_CONFIRMED" and event.edge:
                self._add_connection(
                    event.edge.source,
                    event.edge.target,
                    event.edge.edge_type
                )

    def add_edge(self, edge: EdgeDef):
        """Add an edge from a proposal confirmation."""
        self._add_connection(edge.source, edge.target, edge.edge_type)

    def _add_connection(self, source: str, target: str, edge_label: str):
        # 1. Add File Node (Gold Square with Glow)
        if source not in self.graph:
            self.graph.add_node(
                source,
                label=source,
                color=self.c_file,
                shape="square",
                size=25,
                title=f"File: {source}",
                shadow={'enabled': True, 'color': self.c_file, 'size': 15, 'x': 0, 'y': 0},
                font={'face': 'Courier New', 'color': 'white', 'size': 16},
                node_type="file"
            )

        # 2. Add Intent Node (Pink Dot with Glow)
        if target not in self.graph:
            self.graph.add_node(
                target,
                label=target,
                color=self.c_intent,
                shape="dot",
                size=15,
                title=f"Intent: {target}",
                shadow={'enabled': True, 'color': self.c_intent, 'size': 20, 'x': 0, 'y': 0},
                font={'face': 'Courier New', 'color': 'white', 'size': 14},
                node_type="intent"
            )

        # 3. Add Edge (White Fiber Optic)
        # Increase width based on 'weight' (how many times confirmed)
        weight = 1
        if self.graph.has_edge(source, target):
            weight = self.graph[source][target].get('width', 1) + 1

        self.graph.add_edge(
            source,
            target,
            width=weight,
            title=f"Strength: {weight}",
            label=edge_label,
            color={'color': 'white', 'opacity': 0.6},
            font={'align': 'middle', 'face': 'Courier New', 'color': 'gray', 'size': 10}
        )

    def get_stats(self) -> dict:
        """Get graph statistics."""
        nodes = list(self.graph.nodes(data=True))
        return {
            "total_nodes": len(nodes),
            "files": sum(1 for _, d in nodes if d.get("node_type") == "file"),
            "intents": sum(1 for _, d in nodes if d.get("node_type") == "intent"),
            "edges": self.graph.number_of_edges()
        }

    def manifest(self, output_file: str = "angel_traceability.html"):
        """Generate the cyber-aesthetic HTML visualization."""
        # Dark Mode Background
        net = Network(height="100vh", width="100%", bgcolor="#000000", font_color="white")
        net.from_nx(self.graph)

        # --- THE PHYSICS ENGINE ---
        # BarnesHut is stable for large graphs with gentle breathing motion
        options = """
        {
          "nodes": {
            "borderWidth": 2,
            "borderWidthSelected": 4
          },
          "edges": {
            "smooth": {
              "type": "continuous",
              "forceDirection": "none"
            }
          },
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -3000,
              "centralGravity": 0.3,
              "springLength": 150,
              "springConstant": 0.04,
              "damping": 0.09,
              "avoidOverlap": 0.2
            },
            "minVelocity": 0.75
          }
        }
        """
        net.set_options(options)

        net.save_graph(output_file)
        return output_file
