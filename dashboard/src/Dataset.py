import os
import pandas
import config
import zipfile
import requests
from tqdm import tqdm


# Variables for loading remote datasets
DATASET_URLS = {
    "gtzan": "https://huggingface.co/datasets/danilotpnta/GTZAN_genre_classification/resolve/main/gtzan.zip",
}


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


class Dataset:

    data = None
    count = None
    attr_data = None

    @staticmethod
    def load(metadata_csv: str):

        Dataset.data = pandas.read_csv(
            metadata_csv
        )  # .sample(frac=0.1, random_state=42)
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
                url = DATASET_URLS[folder]

            except Exception as e:
                print(
                    f"Dataset '{folder}' not found online. If this is a local dataset, please place the folder in 'dashboard/data'!"
                )

            download_url(url, config.DATA_DIR)
            extract_zip(config.DATA_DIR, config.DATA_DIR)

        else:
            print("Dataset already present. Skipping step...")

        pass
