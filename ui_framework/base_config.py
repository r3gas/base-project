import os
from pathlib import Path
import platform

browser = "chrome"

# Tests will run headless if not running locally
if platform.system() == "Darwin":
    headless = False
else:
    headless = True

def get_project_root():
    return Path(__file__).parent
