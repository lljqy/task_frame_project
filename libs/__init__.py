import os
import importlib

settings = importlib.import_module(os.environ.get('GLOBAL_SETTINGS'))