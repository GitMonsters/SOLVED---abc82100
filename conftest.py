import sys
import os

# Ensure the repo root is on sys.path so that solver, analysis, and verify
# can be imported from the tests/ subdirectory.
sys.path.insert(0, os.path.dirname(__file__))
