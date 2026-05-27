import sys
import os
from pathlib import Path

# Add project root to sys.path so the backend module can be found
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the FastAPI app
from backend.main import app
