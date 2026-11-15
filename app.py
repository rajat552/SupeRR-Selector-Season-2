"""
Root entry point for SupeRR Selector Season 2 Streamlit App.
Redirects execution to dashboard/app.py.
"""
import sys
import importlib.util
from pathlib import Path

# Add project root to sys.path so all imports resolve correctly
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load dashboard/app.py as a module
dashboard_path = project_root / "dashboard" / "app.py"
spec = importlib.util.spec_from_file_location("dashboard_app", str(dashboard_path))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
