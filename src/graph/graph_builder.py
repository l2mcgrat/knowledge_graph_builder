
import json
from pathlib import Path

import networkx as nx


DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DOCS_PATH = DATA_DIR / "docs.json"


def build_graph():
    G = nx.Graph()

    # Root
    G.add_node("Knowledge")

    subjects = [
        "Philosophy",
        "Math",
        "Physics",
        "Chemistry",
        "Biology",
        "Psychology",
        "Engineering",
        "Business",
        "Economics",
    ]

    for subj in subjects:
        G.add_node(subj)
        G.add_edge("Knowledge", subj)

    # Chemistry branches
    chem_branches = [
        "Organic Chemistry",
        "Inorganic Chemistry",
        "Physical Chemistry",
        "Biochemistry",
    ]
    for branch in chem_branches:
        G.add_node(branch)
        G.add_edge("Chemistry", branch)

    # Example overlap
    G.add_node("Thermodynamics")
    G.add_edge("Physical Chemistry", "Thermodynamics")
    G.add_edge("Physics", "Thermodynamics")
    G.add_edge("Thermodynamics", "Engineering")

    # Statistical mechanics as a bridge between
    # Thermodynamics and Physical Chemistry
    G.add_node("Statistical Mechanics")
    G.add_edge("Thermodynamics", "Statistical Mechanics")
    G.add_edge("Statistical Mechanics", "Physical Chemistry")

    # Load document nodes from JSON so they can scale
    # independently of this Python file.
    if DOCS_PATH.exists():
        with DOCS_PATH.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        for doc in payload.get("documents", []):
            label = doc.get("label")
            if not label:
                continue

            # Everything except id/label/concepts becomes
            # node attributes (e.g. pdf_file, tex_file).
            attrs = {
                k: v
                for k, v in doc.items()
                if k not in {"id", "label", "concepts"}
            }

            G.add_node(label, **attrs)

            for concept in doc.get("concepts", []):
                if concept not in G:
                    G.add_node(concept)
                G.add_edge(concept, label)

    return G
