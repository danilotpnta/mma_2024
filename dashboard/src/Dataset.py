import os
import pandas
import config
import zipfile
import requests
from tqdm import tqdm

# Helper functions
def download_url(url, output_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    with open(output_path, "wb") as file, tqdm(
        desc="Downloading dataset",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))

def extract_zip(file_path, extract_path):
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        for member in tqdm(zip_ref.infolist(), desc="Extracting dataset"):
            zip_ref.extract(member, extract_path)

def create_symlinks(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created target directory: {target_dir}")

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(source_file, source_dir)
            target_file = os.path.join(target_dir, relative_path)

            target_file_dir = os.path.dirname(target_file)
            if not os.path.exists(target_file_dir):
                os.makedirs(target_file_dir)
                print(f"Created directory: {target_file_dir}")

            if not os.path.exists(target_file):
                os.symlink(source_file, target_file)
                # print(f"Symlink created: {target_file} -> {source_file}")
            else:
                print(f"Symlink already exists: {target_file} -> {source_file}")

class Dataset:
    data = None
    count = None
    attr_data = None

    @staticmethod
    def load(metadata_csv: str):
        Dataset.data = pandas.read_csv(
            metadata_csv
        )
        Dataset.data.reset_index(drop=True, inplace=True)
        Dataset.data.drop(columns=["id"], inplace=True)
        Dataset.data["id"] = Dataset.data.index

    @staticmethod
    def get():
        return Dataset.data

    @staticmethod
    def get_attr_data():
        return Dataset.attr_data

    @staticmethod
    def class_count():
        return Dataset.count

    @staticmethod
    def metadata_exist(folder: str):
        metadata_path = os.path.join(config.DATA_DIR, f"{folder}/metadata.csv")
        return os.path.isfile(metadata_path)

    @staticmethod
    def download(folder: str):
        # Check if the dataset is already downloaded and extracted
        data_folder = os.path.join(config.DATA_DIR, folder)
        dataset_present = (
            os.path.isdir(data_folder) and not os.listdir(data_folder) == []
        )

        if not dataset_present:
            # Download and extract the dataset
            try:
                url = config.DATASET_URLS[folder]
            except Exception as e:
                print(
                    f"Dataset '{folder}' not found online. If this is a local dataset, please place the folder in 'dashboard/data'!"
                )
                return

            zip_path = os.path.join(config.DATA_DIR, f"{folder}.zip")
            download_url(url, zip_path)
            extract_zip(zip_path, config.DATA_DIR)
            os.remove(zip_path)  # Clean up the zip file after extraction

        else:
            print("Dataset already present. Skipping download and extraction...")

        # Check if the symlinks are created
        source_dir = os.path.join(config.DATA_DIR, folder, "genres")
        target_dir = os.path.join("dashboard", "src", "assets", "genres")
        symlink_created = any(os.path.islink(os.path.join(target_dir, f)) for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)))

        if not symlink_created:
            print("Symlinks not found. Creating symlinks...")
            create_symlinks(source_dir, target_dir)
        else:
            print("Symlinks already created. Skipping symlink creation...")

        return
