
import streamlit as st
from pyvis.network import Network
import networkx as nx
import os, sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.graph.graph_builder import build_graph
from src.utils.config import PDF_DIR

def visualize_graph(G):
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(G)

    net.write_html("graph.html")

    # Display in Streamlit
    with open("graph.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=600, scrolling=True)

def main():
    st.title("Knowledge Graph Builder")
    st.write("Explore subjects, branches, and overlaps in your knowledge graph.")

    G = build_graph()
    visualize_graph(G)

    st.subheader("Reference documents")
    for node_label, attrs in G.nodes(data=True):
        pdf_file = attrs.get("pdf_file")
        tex_file = attrs.get("tex_file")

        if pdf_file:
            pdf_path = PDF_DIR / pdf_file
            if pdf_path.exists():
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label=f"Download {node_label} (PDF)",
                        data=f,
                        file_name=pdf_path.name,
                        mime="application/pdf",
                    )
            else:
                st.write(f"{node_label} PDF not found at {pdf_path}")

        if tex_file:
            tex_path = PDF_DIR / tex_file
            if tex_path.exists():
                with open(tex_path, "rb") as f:
                    st.download_button(
                        label=f"Download {node_label} (TeX)",
                        data=f,
                        file_name=tex_path.name,
                        mime="text/x-tex",
                    )
            else:
                st.write(f"{node_label} TeX not found at {tex_path}")

if __name__ == "__main__":
    main()

