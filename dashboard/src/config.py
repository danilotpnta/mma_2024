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
    "gtzan": "https://huggingface.co/datasets/danilotpnta/GTZAN_genre_classification/resolve/main/data/gtzan.zip",
    "custom_sample": "https://amsuni-my.sharepoint.com/:u:/g/personal/gregory_go_student_uva_nl/EXJx3dH5cYtInbtaz8kOUGUBCXRUnmD4qp46i4zYUsl8mg?e=eixhyj&download=1",
}

# Others
# DATASET_PATH = os.path.join(DATA_DIR, "dataset.csv")
# DATASET_PATH = os.path.join(DATA_DIR, "gtzan/metadata_aug.csv")
DATASET_PATH = os.path.join(DATA_DIR, "metadata.csv")
BASE_URL = "https://amsuni-my.sharepoint.com/:f:/r/personal/oliver_neut_student_uva_nl/Documents/Audio-MMA"

PROSONO_LOGO = "assets/ProSono.png"

GENRE_COLORS = {
    "hiphop": "rgb(99, 110, 250)",
    "pop": "rgb(239, 85, 59)",
    "country": "rgb(0, 204, 150)",
    "disco": "rgb(171, 99, 250)",
    "jazz": "rgb(255, 161, 90)",
    "reggae": "rgb(25, 211, 243)",
    "metal": "rgb(255, 102, 146)",
    "rock": "rgb(182, 232, 128)",
    "blues": "rgb(255, 151, 255)",
    "classical": "rgb(254, 203, 82)",
}
