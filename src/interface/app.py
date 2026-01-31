
import streamlit as st
from pyvis.network import Network
import networkx as nx
import os, sys
import subprocess
from pathlib import Path

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.graph.graph_builder import build_graph
from src.utils.config import PDF_DIR, PDFLATEX_CMD


def visualize_graph(G):
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(G)

    net.write_html("graph.html")

    # Display in Streamlit
    with open("graph.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=600, scrolling=True)


def _compile_tex_if_needed(tex_path: Path, pdf_path: Path):
    """Compile tex_path to pdf_path if needed.

    We trigger compilation if the .pdf does not exist or if the
    .tex is newer than the .pdf. Any errors are surfaced as a
    Streamlit warning but do not crash the app.
    """

    if not tex_path.exists():
        return

    needs_compile = not pdf_path.exists()
    if not needs_compile:
        try:
            needs_compile = tex_path.stat().st_mtime > pdf_path.stat().st_mtime
        except OSError:
            needs_compile = False

    if not needs_compile:
        return

    # Keep LaTeX aux/log/out files in a dedicated subfolder
    aux_dir = tex_path.parent / "aux"
    try:
        aux_dir.mkdir(exist_ok=True)
    except OSError:
        # If we can't create the aux directory, fall back to
        # the default behaviour (files next to the .tex file).
        aux_dir = tex_path.parent

    try:
        result = subprocess.run(
            [PDFLATEX_CMD, f"--aux-directory={aux_dir.name}", tex_path.name],
            cwd=str(tex_path.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60,
        )
    except Exception as exc:  # pragma: no cover - runtime safety
        st.warning(f"Could not run LaTeX compiler: {exc}")
        return

    if result.returncode != 0:
        st.warning(
            "LaTeX compilation failed for "
            f"{tex_path.name} (return code {result.returncode})."
        )

def main():
    st.title("Knowledge Graph Builder")
    st.write("Explore subjects, branches, and overlaps in your knowledge graph.")

    G = build_graph()
    visualize_graph(G)

    # --- Dynamic reference documents section ---
    # We treat any node with pdf_file/tex_file metadata as a
    # "document node", and allow the user to either select the
    # document directly, or select the conceptual edge that it
    # connects (e.g. Statistical Mechanics  Physical Chemistry).

    st.subheader("Reference documents")

    # Collect document nodes
    doc_nodes = {
        node_label: attrs
        for node_label, attrs in G.nodes(data=True)
        if attrs.get("pdf_file") or attrs.get("tex_file")
    }

    if not doc_nodes:
        st.write("No document nodes defined in the graph.")
        return

    # Build edge-based view: for each document node, look at the
    # concepts it connects and expose them as selectable "edges".
    # Multiple documents can live on the same conceptual edge, so
    # we group docs by the unordered pair of their neighbouring
    # concept nodes.
    edge_to_docs = {}
    for doc_label in doc_nodes.keys():
        neighbors = list(G.neighbors(doc_label))
        if len(neighbors) < 2:
            continue
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                u, v = neighbors[i], neighbors[j]
                a, b = sorted([u, v])
                key = f"{a} ↔ {b}"
                edge_to_docs.setdefault(key, []).append(doc_label)

    edge_options = sorted(edge_to_docs.keys())

    mode = st.radio("Show documents by:", ["Node", "Edge"])

    selected_doc_label = None

    if mode == "Node":
        selected_doc_label = st.selectbox(
            "Select a document node", sorted(doc_nodes.keys())
        )
    else:  # Edge mode
        if not edge_options:
            st.info("No edges with associated documents yet.")
        else:
            selected_edge = st.selectbox(
                "Select an edge (concept pair)", edge_options
            )
            docs_for_edge = edge_to_docs.get(selected_edge, [])
            if not docs_for_edge:
                st.info("No documents attached to this edge yet.")
            elif len(docs_for_edge) == 1:
                selected_doc_label = docs_for_edge[0]
            else:
                selected_doc_label = st.selectbox(
                    "Select a document on this edge", sorted(docs_for_edge)
                )

    if not selected_doc_label:
        return

    attrs = doc_nodes[selected_doc_label]
    pdf_file = attrs.get("pdf_file")
    tex_file = attrs.get("tex_file")

    tex_path = PDF_DIR / tex_file if tex_file else None
    pdf_path = PDF_DIR / pdf_file if pdf_file else None

    # Auto-compile TeX to PDF when possible and needed.
    if tex_path is not None and pdf_path is not None:
        _compile_tex_if_needed(tex_path, pdf_path)

    if pdf_path is not None:
        if pdf_path.exists():
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label=f"Download {selected_doc_label} (PDF)",
                    data=f,
                    file_name=pdf_path.name,
                    mime="application/pdf",
                )
        else:
            st.write(f"{selected_doc_label} PDF not found at {pdf_path}")

if __name__ == "__main__":
    main()

