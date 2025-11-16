
import networkx as nx

def build_graph():
    G = nx.Graph()

    # Root
    G.add_node("Knowledge")

    subjects = ["Philosophy", "Math", "Physics", "Chemistry", 
                "Biology", "Psychology", "Engineering", "Business", "Economics"]

    for subj in subjects:
        G.add_node(subj)
        G.add_edge("Knowledge", subj)

    # Chemistry branches
    chem_branches = ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Biochemistry"]
    for branch in chem_branches:
        G.add_node(branch)
        G.add_edge("Chemistry", branch)

    # Example overlap
    G.add_node("Thermodynamics")
    G.add_edge("Physical Chemistry", "Thermodynamics")
    G.add_edge("Physics", "Thermodynamics")
    G.add_edge("Thermodynamics", "Engineering")

    return G
