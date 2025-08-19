import sys
import os

# Add the project root directory to the Python path
# This allows for absolute imports from the project root (e.g., `from core import config`)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
