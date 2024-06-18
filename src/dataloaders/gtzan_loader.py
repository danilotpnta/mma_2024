import os
import sys
import requests
import shutil
import zipfile
from tqdm import tqdm
from pathlib import Path
from config import DATASET_DIR, DATA_DIR, DOWNLOADS_DIR

DATASET_URLS = {
    "gtzan": "https://huggingface.co/datasets/danilotpnta/GTZAN_genre_classification/resolve/main/gtzan.zip",
}

DOWNLOAD_PATHS = {
    "gtzan": DOWNLOADS_DIR / "gtzan.zip",
}

def download_url(url, output_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(output_path, 'wb') as file, tqdm(
        desc='Downloading dataset',
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))

def extract_zip(file_path, extract_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for member in tqdm(zip_ref.infolist(), desc='Extracting dataset'):
            zip_ref.extract(member, extract_path)

def load():
    print("Loading GTZAN dataset!")
    
    # Ensure directories exist
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

    download_path = DOWNLOAD_PATHS["gtzan"]
    url = DATASET_URLS["gtzan"]

    # Check if the dataset is already downloaded and extracted
    dataset_extracted = DATA_DIR.is_dir() and any(DATA_DIR.iterdir())

    if not dataset_extracted:
        # Clean up existing data
        shutil.rmtree(DATA_DIR, ignore_errors=True)
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Download the dataset
        download_url(url, download_path)

        # Extract the dataset
        extract_zip(download_path, DATA_DIR)

        # Remove the zip file after extraction
        os.remove(download_path)

    else:
        print("Dataset already downloaded and unzipped, skipping step...")

    print("Finished loading datasets!")

if __name__ == "__main__":
    load()
