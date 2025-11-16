# Links

import networkx as nx

# Initialize graph
G = nx.Graph()

# Root node
G.add_node("Knowledge")

# Subjects
subjects = ["Philosophy", "Math", "Physics", "Chemistry", 
            "Biology", "Psychology", "Engineering", "Business", "Economics"]

for subj in subjects:
    G.add_node(subj)
    G.add_edge("Knowledge", subj)

# Example branches
chem_branches = ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Biochemistry"]
for branch in chem_branches:
    G.add_node(branch)
    G.add_edge("Chemistry", branch)

# Example areas
areas = ["Thermodynamics", "Quantum Mechanics"]
for area in areas:
    G.add_node(area)
    G.add_edge("Physical Chemistry", area)
    G.add_edge("Physics", area)  # Overlap

# Application edges
G.add_edge("Thermodynamics", "Engineering")
G.add_edge("Biochemistry", "Business")
