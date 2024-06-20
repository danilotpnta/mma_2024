import os
from pathlib import Path


IMAGE_GALLERY_SIZE = 8
IMAGE_GALLERY_ROW_SIZE = 4

DEFAULT_PROJECTION = "UMAP"

SCATTERPLOT_COLOR = 'rgba(31, 119, 180, 0.5)'
SCATTERPLOT_SELECTED_COLOR = 'red'

# Path configuration
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Others
# DATASET_PATH = os.path.join(DATA_DIR, "dataset.csv")
DATASET_PATH = os.path.join(DATA_DIR, "gtzan/metadata_aug.csv")

