"""
Root entry point for SupeRR Selector Season 2 Streamlit App.
Redirects execution to dashboard/app.py.
"""
import runpy
from pathlib import Path

dashboard_app = Path(__file__).parent / "dashboard" / "app.py"
runpy.run_path(str(dashboard_app), run_name="__main__")
