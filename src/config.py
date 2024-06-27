import os
from pathlib import Path

IMAGE_GALLERY_SIZE = 8
IMAGE_GALLERY_ROW_SIZE = 4

DEFAULT_PROJECTION = "umap"

SCATTERPLOT_COLOR = "rgba(31, 119, 180, 0.5)"
SCATTERPLOT_SELECTED_COLOR = "red"

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


# Path configuration
ROOT_DIR = Path(__file__).parent.parent
DATASET_DIR = os.path.join(ROOT_DIR, "dataset")
DATA_DIR = os.path.join(DATASET_DIR, "data")
DOWNLOADS_DIR = os.path.join(DATASET_DIR, "downloads")

# Others
DATASET_PATH = os.path.join(DATA_DIR, "dataset.csv")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
AUGMENTED_DATASET_PATH = os.path.join(DATA_DIR, "augmented_dataset.csv")
ATTRIBUTE_DATA_PATH = os.path.join(DATA_DIR, "image_attributes.csv")

SAMPLE_DATASET_PATH = os.path.join(DATASET_DIR, "sample_data/first_100.csv")

# FMA
NUM_CLASSES = 8  # for FMA Small
AUDIO_DIR = os.path.join(DATA_DIR, "fma_small_wav")
AUDIO_METADATA_DIR = os.path.join(DATA_DIR, "fma_metadata")

TRACKS_PATH = os.path.join(AUDIO_METADATA_DIR, "tracks.csv")
FEATURES_PATH = os.path.join(AUDIO_METADATA_DIR, "features.csv")
ECHONEST_PATH = os.path.join(AUDIO_METADATA_DIR, "echonest.csv")

# Train
CHECKPOINT_DIR = os.path.join(ROOT_DIR, "checkpoints")
BATCH_SIZE: int = 32
EPOCHS: int = 10
LEARNING_RATE = 0.001
