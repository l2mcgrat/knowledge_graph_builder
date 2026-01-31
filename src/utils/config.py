

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

# Folder to store reference PDFs for the knowledge graph.
PDF_DIR = BASE_DIR / "pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# LaTeX engine command used to compile .tex to .pdf.
# By default we assume "pdflatex" is on PATH, but you can
# override this with the PDFLATEX_CMD environment variable
# (for example, set it to the full path of pdflatex.exe).
PDFLATEX_CMD = os.environ.get("PDFLATEX_CMD", "pdflatex")


