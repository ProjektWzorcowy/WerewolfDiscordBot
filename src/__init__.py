import os
import importlib

# Dynamically import all modules in the src folder
current_dir = os.path.dirname(__file__)
files = [f[:-3] for f in os.listdir(current_dir) if f.endswith(".py") and f != "__init__.py"]

for file in files:
    importlib.import_module(f"src.{file}")
