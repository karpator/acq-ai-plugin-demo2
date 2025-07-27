"""
Shared module with plugin system support.

This module can run independently or as part of a larger system with country-specific plugins.
When running within the shared/ directory, it uses direct imports.
When accessed from outside, it uses the full module path.
"""

import sys
from pathlib import Path

# Configure Python path for internal shared module imports
# Only add to path when running from within shared directory
current_dir = Path(__file__).parent
if current_dir.name == "shared":
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

__version__ = "1.0.0"
__author__ = "Plugin System"
