from pathlib import Path

# Project root directory
BASE_DIR: Path = Path(__file__).resolve()

# Data storage paths
DATA_DIR: Path = BASE_DIR / ".data"
TASKS_FILE_PATH: Path = DATA_DIR / "tasks.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)
