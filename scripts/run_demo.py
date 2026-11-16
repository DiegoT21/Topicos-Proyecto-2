"""Arranca la API y la interfaz web en http://localhost:8000 (desde cualquier carpeta).

    python scripts/run_demo.py          # usa tutorias.db en la raíz del repo
Antes, si quieres datos de ejemplo:  python src/seed_demo.py --reset
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)  # la BD por defecto (sqlite:///./tutorias.db) queda en la raíz del repo
sys.path.insert(0, str(ROOT / "src"))

import uvicorn  # noqa: E402

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=int(os.environ.get("PORT", "8000")))
