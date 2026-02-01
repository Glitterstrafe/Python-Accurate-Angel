import networkx as nx
from pyvis.network import Network
from typing import List, Optional
from .types import AngelEvent, EdgeDef


class Sephirot:
    """
    The Knowledge Graph. Tracks the lineage of code.
    State is derived entirely from the Chronicles (event log).
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        # Theme colors
        self.c_file = "#FFD700"     # Gold - Files
        self.c_intent = "#FF69B4"   # Pink - Intents
        self.c_agent = "#87CEEB"    # Sky Blue - Agent actions
        self.c_edge = "#FFFFFF"     # White - Connections

        # Edge type colors
        self.edge_colors = {
            "implements": "#00FF00",  # Green
            "modifies": "#FFA500",    # Orange
            "deprecates": "#FF0000",  # Red
            "relates_to": "#FFFFFF"   # White
        }

    def clear(self):
        """Clear the graph for rebuilding."""
        self.graph.clear()

    def add_file_node(self, filename: str):
        """Add a file node (Gold square)."""
        if filename not in self.graph:
            self.graph.add_node(
                filename,
                label=filename,
                color=self.c_file,
                shape="square",
                size=25,
                node_type="file"
            )

    def add_intent_node(self, intent_label: str):
        """Add an intent node (Pink circle)."""
        if intent_label not in self.graph:
            self.graph.add_node(
                intent_label,
                label=intent_label,
                color=self.c_intent,
                shape="dot",
                size=20,
                node_type="intent"
            )

    def add_edge(self, edge: EdgeDef):
        """Add a typed edge between nodes."""
        # Ensure both nodes exist
        self.add_file_node(edge.source)
        self.add_intent_node(edge.target)

        # Add the edge with styling
        edge_color = self.edge_colors.get(edge.edge_type, self.c_edge)
        self.graph.add_edge(
            edge.source,
            edge.target,
            color=edge_color,
            title=edge.edge_type,
            edge_type=edge.edge_type
        )

    def add_event(self, agent_thought: str, affected_file: str):
        """
        Legacy method: Links a thought to a file.
        Kept for backward compatibility.
        """
        thought_id = f"Thought_{len([n for n in self.graph.nodes if n.startswith('Thought_')])}"

        self.graph.add_node(
            thought_id,
            label="Agent Action",
            title=agent_thought,
            color=self.c_agent,
            shape="dot",
            size=15,
            node_type="action"
        )

        self.add_file_node(affected_file)
        self.graph.add_edge(thought_id, affected_file, color=self.c_edge)

    def rebuild_from_chronicles(self, events: List[AngelEvent]):
        """
        Rebuild the entire graph state from the event log.
        This is the core of event sourcing - state derived from events.
        """
        self.clear()

        for event in events:
            if event.action_type == "PROPOSAL_CONFIRMED" and event.edge:
                self.add_edge(event.edge)
            elif event.action_type == "INTENT_CREATED" and event.intent_label:
                self.add_intent_node(event.intent_label)
            elif event.action_type == "WORK_UNIT_CAPTURED" and event.file_path:
                self.add_file_node(event.file_path)

    def rebuild_to_timestamp(self, events: List[AngelEvent], timestamp: str):
        """
        Rebuild graph state up to a specific timestamp.
        Enables "Time Travel" feature.
        """
        filtered = [e for e in events if e.timestamp <= timestamp]
        self.rebuild_from_chronicles(filtered)

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
        """Generates the interactive HTML visualization."""
        net = Network(
            height="750px",
            width="100%",
            bgcolor="#000000",
            font_color="white"
        )

        # Convert NetworkX graph to Pyvis
        net.from_nx(self.graph)

        # Physics options for "floaty space" feel
        net.force_atlas_2based(
            gravity=-50,
            central_gravity=0.01,
            spring_length=100,
            spring_strength=0.08
        )

        # Add legend
        net.add_node(
            "legend_file", label="File", color=self.c_file,
            shape="square", size=10, x=-200, y=-200, fixed=True
        )
        net.add_node(
            "legend_intent", label="Intent", color=self.c_intent,
            shape="dot", size=10, x=-200, y=-170, fixed=True
        )

        net.save_graph(output_file)
        return output_file
