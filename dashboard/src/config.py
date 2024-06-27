import os
from pathlib import Path


IMAGE_GALLERY_SIZE = 8
IMAGE_GALLERY_ROW_SIZE = 4

DEFAULT_PROJECTION = "umap"

SCATTERPLOT_COLOR = "rgba(31, 119, 180, 0.5)"
SCATTERPLOT_SELECTED_COLOR = "red"

# Path configuration
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Variables for loading remote datasets
DATASET_URLS = {
    "gtzan": "https://huggingface.co/datasets/danilotpnta/GTZAN_genre_classification/resolve/main/gtzan.zip",
    "custom_sample": "https://amsuni-my.sharepoint.com/:u:/g/personal/gregory_go_student_uva_nl/EXJx3dH5cYtInbtaz8kOUGUBCXRUnmD4qp46i4zYUsl8mg?e=eixhyj&download=1",
}

# Others
# GTZAN default paths
DATASET_PATH = os.path.join(DATA_DIR, "gtzan/metadata.csv")
