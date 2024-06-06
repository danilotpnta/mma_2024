import os
import sys
import wget
import shutil
import zipfile
from src import config

DATASET_URLS = {
    "fma_small": "https://os.unil.cloud.switch.ch/fma/fma_small.zip",
    "fma_metadata": "https://os.unil.cloud.switch.ch/fma/fma_metadata.zip"
}
DOWNLOAD_PATHS = {
    "fma_small": os.path.join(config.DOWNLOADS_DIR, "fma_small.zip"),
    "fma_metadata": os.path.join(config.DOWNLOADS_DIR, "fma_metadata.zip")
}

def download_dataset(url, path):
    def bar_progress(current, total, _):
        sys.stdout.write(
            "\r"
            + "Downloading: %d%% [%d / %d] bytes"
            % (current / total * 100, current, total)
        )
        sys.stdout.flush()

    if not os.path.isfile(path):
        print(f"Downloading dataset from {url} to {path}")
        wget.download(url, bar=bar_progress, out=path)
    else:
        print(f"File already exists at {path}, skipping download")

def extract_dataset(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def load():
    if not os.path.isdir(config.DATASET_DIR):
        os.makedirs(config.DATASET_DIR)
    shutil.rmtree(config.DATA_DIR, ignore_errors=True)
    os.makedirs(config.DATA_DIR)
    os.makedirs(config.DOWNLOADS_DIR, exist_ok=True)
    
    for name, url in DATASET_URLS.items():
        download_path = DOWNLOAD_PATHS[name]
        download_dataset(url, download_path)
        
        final_path = os.path.join(config.DATA_DIR, name)
        if not os.path.isdir(final_path):
            os.makedirs(final_path)
        
        print(f"Extracting data from {download_path} to {final_path}")
        extract_dataset(download_path, final_path)

    print("Done loading datasets!")
    
def cleanup():
    print("Performing cleanup tasks if any")

if __name__ == "__main__":
    load()
    # cleanup()
