import os
from pathlib import Path


IMAGE_GALLERY_SIZE = 8
IMAGE_GALLERY_ROW_SIZE = 4

DEFAULT_PROJECTION = "UMAP"

# Path configuration
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Others
DATASET_PATH = os.path.join(DATA_DIR, "dataset.csv")