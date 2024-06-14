import os
from pathlib import Path


DEFAULT_PROJECTION = "UMAP"

# Path configuration
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Others
DATASET_PATH = os.path.join(DATA_DIR, "dataset.csv")