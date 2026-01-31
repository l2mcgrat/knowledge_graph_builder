
import networkx as nx


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

    # Document node for the full ideal gas law derivation.
    # Both the compiled PDF and the TeX source live in the
    # pdfs/ folder and are mapped as metadata on this node.
    G.add_node(
        "Ideal Gas Law",
        node_type="doc",
        pdf_file="ideal_gas_law_stat_mech.pdf",
        tex_file="ideal_gas_law_full_derivation.tex",
    )
    G.add_edge("Statistical Mechanics", "Ideal Gas Law")
    G.add_edge("Ideal Gas Law", "Physical Chemistry")

    return G
