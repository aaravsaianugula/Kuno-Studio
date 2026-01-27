import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Resolve path relative to this file (backend/app/utils/project_state.py)
# We want to store it in backend/ (parent of app) or backend/data
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_STATE_FILE = BASE_DIR / "current_project.json"

def save_project_state(state: Dict[str, Any]):
    """Saves the current project state to a JSON file."""
    try:
        with open(PROJECT_STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Failed to save project state: {e}")

def load_project_state() -> Optional[Dict[str, Any]]:
    """Loads the current project state from a JSON file."""
    if not os.path.exists(PROJECT_STATE_FILE):
        return None
    try:
        with open(PROJECT_STATE_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load project state: {e}")
        return None
