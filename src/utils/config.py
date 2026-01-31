

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

# Folder to store reference PDFs for the knowledge graph.
PDF_DIR = BASE_DIR / "pdfs"
os.makedirs(PDF_DIR, exist_ok=True)


