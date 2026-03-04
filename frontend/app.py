import os
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)  # keeps all your existing relative paths working

runpy.run_path(str(ROOT / "app.py"), run_name="__main__")