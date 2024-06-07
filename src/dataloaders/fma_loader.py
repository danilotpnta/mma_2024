import os
import sys
import wget
import shutil
import zipfile
from tqdm import tqdm
from src import config
from src.utils.audio_utils import convert_mp3_to_wav

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

def convert_all_mp3_to_wav(mp3_dir, wav_dir):

    # collect all MP3 files to process
    mp3_files = []
    for root, _, files in os.walk(mp3_dir):
        for file in files:
            if file.endswith('.mp3'):
                mp3_path = os.path.join(root, file)
                relative_path = os.path.relpath(mp3_path, mp3_dir)
                wav_path = os.path.join(wav_dir, os.path.splitext(relative_path)[0] + '.wav')
                mp3_files.append((mp3_path, wav_path))

    # convert mp3 to wav 
    for mp3_path, wav_path in tqdm(mp3_files, desc="Converting MP3 to WAV"):
        os.makedirs(os.path.dirname(wav_path), exist_ok=True)
        convert_mp3_to_wav(mp3_path, wav_path)

def load():
    mp3_dir = os.path.join(config.DATA_DIR, "fma_small")
    wav_dir = os.path.join(config.DATA_DIR, "fma_small_wav")

    if not os.path.isdir(config.DATASET_DIR):
        os.makedirs(config.DATASET_DIR)
    if not os.path.isdir(config.DOWNLOADS_DIR):
        os.makedirs(config.DOWNLOADS_DIR)

    # Check if dataset is already downloaded and extracted
    dataset_extracted = os.path.isdir(mp3_dir) and os.path.isdir(os.path.join(config.DATA_DIR, "fma_metadata"))

    if not dataset_extracted:
        shutil.rmtree(config.DATA_DIR, ignore_errors=True)
        os.makedirs(config.DATA_DIR)
        os.makedirs(mp3_dir, exist_ok=True)

        for name, url in DATASET_URLS.items():
            download_path = DOWNLOAD_PATHS[name]
            download_dataset(url, download_path)

            final_path = os.path.join(config.DATA_DIR, name)
            if not os.path.isdir(final_path):
                os.makedirs(final_path)

            print(f"Extracting data from {download_path} to {final_path}")
            extract_dataset(download_path, final_path)
    else:
        print("Dataset already downloaded and unzipped, skipping this step.")

    # Convert MP3 files to WAV
    dataset_converted = os.path.isdir(wav_dir)
    if not dataset_converted:
        os.makedirs(wav_dir, exist_ok=True)
        print("Converting MP3 songs to WAV format.")
        convert_all_mp3_to_wav(mp3_dir, wav_dir)
    else:
        print("Dataset already converted, skipping this step.")

    print("Done loading datasets!")

def cleanup():
    print("Performing cleanup tasks if any")

if __name__ == "__main__":
    load()
    # cleanup()
