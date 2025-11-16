
import streamlit as st
from pyvis.network import Network
import networkx as nx
from src.graph.graph_builder import build_graph
import sys
print(sys.path)

def visualize_graph(G):
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(G)
    net.show("graph.html")

    # Display in Streamlit
    with open("graph.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=600, scrolling=True)

def main():
    st.title("📚 Knowledge Graph Builder")
    st.write("Explore subjects, branches, and overlaps in your knowledge graph.")

    G = build_graph()
    visualize_graph(G)

if __name__ == "__main__":
    main()

