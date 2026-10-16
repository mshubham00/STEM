import pandas as pd
import networkx as nx
from pyvis.network import Network
from panel import inject_panels

# -----------------------------
# Configurations
# -----------------------------
DATA_FILE = "matrix.csv"
OUTPUT_HTML = "knowledge.html"

SCALE_LEVELS = {
    "meta": 6,
    "femto": 5,
    "atomic": 4,
    "molecular": 3,
    "planetary": 2,
    "biological": 1,
    "technological": 0,
}

DOMAIN_COLORS = {
    "Mathematics": "#2b2b2b",
    "Physics": "#1f77b4",
    "Chemistry": "#ff7f0e",
    "Earth Science": "#2ca02c",
    "Biology": "#d62728",
    "Engineering": "#9467bd",
}

DEFAULT_COLOR = "#7f7f7f"


# Columns required for main knowledge tree
REQUIRED_COLUMNS = {"concept_id","source","target","relationship","domain","scale"}

# Columns required for math pool
REQUIRED_MATH_COLUMNS = {"math_id","math_topic","target_concept","relationship"}

# -----------------------------
# Load Knowledge Tree
# -----------------------------


def load_knowledge_tree(concept_file, math_file=None):
    """
    Load the main knowledge tree CSV and optionally the math meta-layer CSV.

    Parameters:
        concept_file (str): path to main knowledge CSV
        math_file (str): path to math CSV (optional)

    Returns:
        df_concepts (pd.DataFrame): main domain concepts
        df_math (pd.DataFrame or None): math pool if provided
    """
    # Load main concepts
    df_concepts = pd.read_csv(concept_file)
    if not REQUIRED_COLUMNS.issubset(df_concepts.columns):
        raise ValueError(f"Concept CSV must contain columns: {REQUIRED_COLUMNS}")

    if df_concepts["concept_id"].isnull().any():
        raise ValueError("Null concept_id found in concept CSV")

    # Load math CSV if provided
    df_math = None
    if math_file:
        df_math = pd.read_csv(math_file)
        if not REQUIRED_MATH_COLUMNS.issubset(df_math.columns):
            raise ValueError(f"Math CSV must contain columns: {REQUIRED_MATH_COLUMNS}")
        if df_math["math_id"].isnull().any():
            raise ValueError("Null math_id found in math CSV")

    return df_concepts, df_math

# -----------------------------
# Build Graph
# -----------------------------
def build_graph(df_concepts, df_math=None):
    """
    Build a NetworkX DiGraph from domain concepts and optionally math meta-layer.

    Parameters:
        df_concepts (pd.DataFrame): main knowledge tree CSV
        df_math (pd.DataFrame): math pool CSV (optional)

    Returns:
        G (nx.DiGraph): combined graph
    """
    G = nx.DiGraph()

    # -------------------
    # Add domain concept nodes and edges
    # -------------------
    for _, row in df_concepts.iterrows():
        # Add source node with attributes
        G.add_node(
            row["source"],
            concept_id=row["concept_id"],
            domain=row["domain"],
            scale=row["scale"]
        )
        # Add target node (can be same as source)
        if row["target"] not in G:
            G.add_node(row["target"])

        # Add edge
        G.add_edge(
            row["source"],
            row["target"],
            relationship=row["relationship"]
        )

    # -------------------
    # Add math meta-layer nodes and edges
    # -------------------
    if df_math is not None:
        for _, row in df_math.iterrows():
            # Math node
            if row["math_id"] not in G:
                G.add_node(
                    row["math_id"],
                    concept_id=row["math_id"],
                    domain="Mathematics",
                    scale="meta",
                    label=row["math_topic"]
                )
            # Edge from math node to target concept
            if row["target_concept"] in G:
                G.add_edge(
                    row["math_id"],
                    row["target_concept"],
                    relationship=row["relationship"]
                )
            else:
                # If target concept missing in graph, add it as placeholder
                G.add_node(row["target_concept"])
                G.add_edge(
                    row["math_id"],
                    row["target_concept"],
                    relationship=row["relationship"]
                )

    return G


# -----------------------------
# Visualize Interactive Graph
# -----------------------------
def visualize_interactive(G, output_html=OUTPUT_HTML):
    net = Network(
        height="100vh",
        width="100%",
        bgcolor="#ffffff",
        font_color="#000000",
        directed=True,
        notebook=False
    )

    net.barnes_hut(
        gravity=-6000,
        central_gravity=0.1,
        spring_length=120,
        spring_strength=0.04,
        damping=0.5
    )

    for node, data in G.nodes(data=True):
        domain = data.get("domain")
        scale = data.get("scale")
        color = DOMAIN_COLORS.get(domain, DEFAULT_COLOR)
        y = SCALE_LEVELS.get(scale, 0) * 200
        shape = "box" if domain=="Mathematics" else "ellipse"
        size = 30 if domain=="Mathematics" else 20
        net.add_node(
            node,
            label=node,
            title=f"Domain: {domain}<br>Scale: {scale}",
            color=color,
            shape=shape,
            size=size,
            y=y,
            physics=False if scale=="meta" else True
        )

    for u, v, data in G.edges(data=True):
        net.add_edge(
            u, v, label=data.get("relationship",""), arrows="to"
        )

    # Write base HTML first
    net.write_html(output_html, notebook=False)

    # Inject panels and JS
    inject_panels(output_html)

# -----------------------------
# Main
# -----------------------------
def main():
    # Load concepts and math meta-layer
    df_concepts, df_math = load_knowledge_tree(
        DATA_FILE, 
        math_file="math.csv"  # path to math CSV
    )

    # Build graph from both
    G = build_graph(df_concepts, df_math)

    # Visualize interactively
    visualize_interactive(G)

    print(f"Interactive knowledge tree generated with panels at: {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
