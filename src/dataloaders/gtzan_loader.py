import os
import sys
import requests
import shutil
import zipfile
from tqdm import tqdm
from pathlib import Path
from src import config

DATASET_URLS = {
    "gtzan": "https://huggingface.co/datasets/danilotpnta/GTZAN_genre_classification/resolve/main/gtzan.zip",
}

DOWNLOAD_PATHS = {
    "gtzan": os.path.join(config.DOWNLOADS_DIR, "gtzan.zip"),
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
    
    print("Loading dataset GTZAN...")
    download_path = DOWNLOAD_PATHS["gtzan"]
    url = DATASET_URLS["gtzan"]

    # Check if the dataset is already downloaded and extracted
    dataset_extracted = os.path.isdir(config.GTZAN_DIR) and not os.listdir(config.GTZAN_DIR) == []

    if not dataset_extracted:

        # Ensure directories exist
        # if not os.path.isdir(config.DATASET_DIR):
        #     os.mkdir(config.DATASET_DIR)
        # shutil.rmtree(config.DATA_DIR, ignore_errors=True)
        # os.mkdir(config.DATA_DIR)
        # if not os.path.isdir(config.DOWNLOADS_DIR):
        #     os.mkdir(config.DOWNLOADS_DIR)
        
        # Download the dataset
        download_url(url, download_path)

        # Extract the dataset
        extract_zip(download_path, config.DATA_DIR)

        # Remove the zip file after extraction
        # os.remove(download_path)

    else:
        print("Dataset already downloaded and unzipped, skipping step...")

    print("Finished loading datasets!")

if __name__ == "__main__":
    load()
